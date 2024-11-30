# Copyright Epic Games, Inc. All Rights Reserved.

import sys
import copy
import site
import argparse
import logging
# TODO: Possibly use new importlib.metadata interface instead
import pkg_resources
from pathlib import Path

import packaging.requirements
from pip_requirements_parser import RequirementsFile, InstallRequirement, EditableRequirement

class RequirementsWriter:
    def __init__(self, remove_hashes: bool = True) -> None:
        self.remove_hashes = remove_hashes
        
    def dumps_name_ver(self, req: InstallRequirement) -> str:
        return req.dumps_name() + req.dumps_extras() + req.dumps_specifier()

    def dumps_req(self, req: InstallRequirement, line_comment: str = None, ignore_line: bool = False) -> str:
        if self.remove_hashes:
            # Remove hashes list and dump requirements
            dump_req = copy.deepcopy(req)
            dump_req.hash_options = []
            dump_req_str = dump_req.dumps()
        else:
            # Dump requirement as single line including hashes (if any)
            dump_req_str = req.requirement_line.dumps()
        
        suffix = ''
        if line_comment:
            suffix = f' # {line_comment}'

        prefix = ''
        if ignore_line:
            prefix = '# '

        return f'{prefix}{dump_req_str}{suffix}'


def write_need_install(in_reqs_file: str, needs_install_file: str, disable_hashes: bool):
    workset = pkg_resources.working_set
    reqfile = RequirementsFile.from_file(in_reqs_file)

    # TODO: Add warnings that options (e.g. --index-url, --extra-index-url) are ignored
    req_writer = RequirementsWriter(remove_hashes=disable_hashes)

    # Setup pip site-packages paths to check if detected packages are updateable
    pip_sitepaths = [Path(p) for p in site.getsitepackages([sys.prefix])]

    out_reqs = list[str]()
    for inst_req in reqfile.requirements:
        if not inst_req.match_marker(inst_req.extras):
            logging.debug(f'Dropped requirement (condition false): {inst_req.dumps()}')
            continue

        if isinstance(inst_req, EditableRequirement):
            logging.warning(f'Editable requirements not allowed: {inst_req.dumps()}')
            continue

        requirement = inst_req.req
        if requirement is None:
            continue

        # TODO: Add duplicate detection with marker version matching

        dist = workset.find(pkg_resources.Requirement.parse(requirement.name))
        if dist is not None:
            dist_path = Path(dist.location)
            bCanUpdate = dist_path in pip_sitepaths
            found_label = f'{dist}[{dist.location}]'
            if dist.version in requirement.specifier:
                if requirement.url is not None:
                    logging.warning(f'Skipping matched url version: {req_writer.dumps_name_ver(inst_req)} (If incorrect: remove installed package or reinstall manually)')
                    out_reqs.append(req_writer.dumps_req(inst_req, line_comment=f'[pkg:ignore]: {found_label}', ignore_line=True))
                else:
                    # Don't comment out installed versions in order to allow pip to detect dependency mismatches
                    logging.debug(f'Found matching installed version: {dist} <=> {req_writer.dumps_name_ver(inst_req)}')
                    out_reqs.append(req_writer.dumps_req(inst_req, line_comment=f'[pkg:check]: {found_label}', ignore_line=False))
            elif not bCanUpdate:
                logging.error(f'Found incompatible non-pip version (cannot update): {dist}[{dist.location}] not in {req_writer.dumps_name_ver(inst_req)}')
                out_reqs.append(req_writer.dumps_req(inst_req, line_comment=f'[pkg:ignore]: {found_label}', ignore_line=True))
            else:
                logging.debug(f'Found incompatible version (updating): {dist}[{dist.location}] not in {req_writer.dumps_name_ver(inst_req)}')
                out_reqs.append(req_writer.dumps_req(inst_req, line_comment=f'[pkg:update]: {found_label}', ignore_line=False))
        else:
            out_reqs.append(req_writer.dumps_req(inst_req, line_comment=f'[pkg:install]', ignore_line=False))

    # Warn about invalid lines (these won't be written to file)
    for invalid_req in reqfile.invalid_lines:
        logging.warning(f'{invalid_req.dumps()}')

    with open(needs_install_file, "wt") as f:
        f.write('\n'.join(out_reqs))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse requirements and relative to pkg_resources working set to determine')
    parser.add_argument('requirements_file', type=str, help='The file containing all python requirements lines from plugin descriptors')
    parser.add_argument('out_file', type=str, help='Output file with merged plugin descriptors')
    parser.add_argument('--disable-hashes', action='store_true', help='Remove all hashes (NOTE: this makes all packages insecure, but partial hashing is equally insecure)')
    parser.add_argument('-v', '--verbose', action='count', dest='verbosity', default=0, help='Verbosity level (-v=info,-vv=debug)')

    args = parser.parse_args()

    # Forward all 
    log_modifier = min(10 * args.verbosity, 20)
    default_level = logging.WARNING
    log_level = default_level - log_modifier

    logging.basicConfig(level=log_level)
    write_need_install(args.requirements_file, args.out_file, args.disable_hashes)
