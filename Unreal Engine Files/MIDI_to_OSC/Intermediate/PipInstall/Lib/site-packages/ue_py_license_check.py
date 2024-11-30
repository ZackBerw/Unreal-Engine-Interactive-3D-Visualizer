# Copyright Epic Games, Inc. All Rights Reserved.

import argparse
import logging
import pkg_resources
import re

from typing import Union


class LicenseType:
    @staticmethod
    def _short_name(name: str) -> Union[str,None]:
        match = re.match('\((.+)\)', name)
        return match.group(1) if match is not None else None

    def __init__(self, name: str, group: bool = False, alt_names: list[str] = []) -> None:
        self.name = name
        self.short_name = LicenseType._short_name(name)
        self.alt_names = [x.casefold() for x in [self.name,self.short_name,*alt_names] if x is not None]
        self.group = group

    def __eq__(self, __value: 'LicenseType') -> bool:
        return isinstance(__value, LicenseType) and (self.name == __value.name)

    def __str__(self) -> str:
        return self.name

    def classifier_str(self) -> str:
        return ' :: '.join(['License', self.name])

class OSILicenseType(LicenseType):
    def __init__(self, name: str, alt_names: list[str] = list[str]()) -> None:
        super(OSILicenseType, self).__init__(name, group=False, alt_names=alt_names)

    def classifier_str(self) -> str:
        return ' :: '.join(['License', 'OSI Approved', self.name])


class LicenseClassifierMap:
    _licenses: list[LicenseType] = [
        LicenseType('Aladdin Free Public License (AFPL)'),
        LicenseType('CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'),
        LicenseType('CeCILL-B Free Software License Agreement (CECILL-B)'),
        LicenseType('CeCILL-C Free Software License Agreement (CECILL-C)'),
        LicenseType('DFSG approved'),
        LicenseType('Eiffel Forum License (EFL)'),
        LicenseType('Free For Educational Use'),
        LicenseType('Free For Home Use'),
        LicenseType('Free To Use But Restricted'),
        LicenseType('Free for non-commercial use'),
        LicenseType('Freely Distributable'),
        LicenseType('Freeware'),
        LicenseType('GUST Font License 1.0'),
        LicenseType('GUST Font License 2006-09-30'),
        LicenseType('Netscape Public License (NPL)'),
        LicenseType('Nokia Open Source License (NOKOS)'),
        LicenseType('OSI Approved', group=True),
        OSILicenseType('Academic Free License (AFL)'),
        OSILicenseType('Apache Software License', alt_names=['Apache','Apache License v2.0']),
        OSILicenseType('Apple Public Source License'),
        OSILicenseType('Artistic License'),
        OSILicenseType('Attribution Assurance License'),
        OSILicenseType('BSD License', alt_names=['BSD', 'new BSD']),
        OSILicenseType('Boost Software License 1.0 (BSL-1.0)', alt_names=['BSL']),
        OSILicenseType('CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)'),
        OSILicenseType('Common Development and Distribution License 1.0 (CDDL-1.0)'),
        OSILicenseType('Common Public License'),
        OSILicenseType('Eclipse Public License 1.0 (EPL-1.0)'),
        OSILicenseType('Eclipse Public License 2.0 (EPL-2.0)'),
        OSILicenseType('Eiffel Forum License'),
        OSILicenseType('European Union Public Licence 1.0 (EUPL 1.0)'),
        OSILicenseType('European Union Public Licence 1.1 (EUPL 1.1)'),
        OSILicenseType('European Union Public Licence 1.2 (EUPL 1.2)'),
        OSILicenseType('GNU Affero General Public License v3', alt_names=['AGPL','AGPLv3']),
        OSILicenseType('GNU Affero General Public License v3 or later (AGPLv3+)'),
        OSILicenseType('GNU Free Documentation License (FDL)'),
        OSILicenseType('GNU General Public License (GPL)'),
        OSILicenseType('GNU General Public License v2 (GPLv2)'),
        OSILicenseType('GNU General Public License v2 or later (GPLv2+)'),
        OSILicenseType('GNU General Public License v3 (GPLv3)'),
        OSILicenseType('GNU General Public License v3 or later (GPLv3+)'),
        OSILicenseType('GNU Lesser General Public License v2 (LGPLv2)'),
        OSILicenseType('GNU Lesser General Public License v2 or later (LGPLv2+)'),
        OSILicenseType('GNU Lesser General Public License v3 (LGPLv3)'),
        OSILicenseType('GNU Lesser General Public License v3 or later (LGPLv3+)'),
        OSILicenseType('GNU Library or Lesser General Public License (LGPL)'),
        OSILicenseType('Historical Permission Notice and Disclaimer (HPND)'),
        OSILicenseType('IBM Public License'),
        OSILicenseType('ISC License (ISCL)'),
        OSILicenseType('Intel Open Source License'),
        OSILicenseType('Jabber Open Source License'),
        OSILicenseType('MIT License', alt_names=['MIT']),
        OSILicenseType('MIT No Attribution License (MIT-0)'),
        OSILicenseType('MITRE Collaborative Virtual Workspace License (CVW)'),
        OSILicenseType('MirOS License (MirOS)'),
        OSILicenseType('Motosoto License'),
        OSILicenseType('Mozilla Public License 1.0 (MPL)'),
        OSILicenseType('Mozilla Public License 1.1 (MPL 1.1)'),
        OSILicenseType('Mozilla Public License 2.0 (MPL 2.0)'),
        OSILicenseType('Mulan Permissive Software License v2 (MulanPSL-2.0)'),
        OSILicenseType('Nethack General Public License'),
        OSILicenseType('Nokia Open Source License'),
        OSILicenseType('Open Group Test Suite License'),
        OSILicenseType('Open Software License 3.0 (OSL-3.0)'),
        OSILicenseType('PostgreSQL License'),
        OSILicenseType('Python License (CNRI Python License)'),
        OSILicenseType('Python Software Foundation License'),
        OSILicenseType('Qt Public License (QPL)'),
        OSILicenseType('Ricoh Source Code Public License'),
        OSILicenseType('SIL Open Font License 1.1 (OFL-1.1)'),
        OSILicenseType('Sleepycat License'),
        OSILicenseType('Sun Industry Standards Source License (SISSL)'),
        OSILicenseType('Sun Public License'),
        OSILicenseType('The Unlicense (Unlicense)'),
        OSILicenseType('Universal Permissive License (UPL)'),
        OSILicenseType('University of Illinois/NCSA Open Source License'),
        OSILicenseType('Vovida Software License 1.0'),
        OSILicenseType('W3C License'),
        OSILicenseType('X.Net License'),
        OSILicenseType('Zope Public License'),
        OSILicenseType('zlib/libpng License', alt_names=['zlib','libpng']),
        LicenseType('Other/Proprietary License', alt_names=['Proprietary']),
        LicenseType('Public Domain'),
        LicenseType('Repoze Public License'),
    ]

    def __init__(self) -> None:
        self.classifier_map = {x.classifier_str(): x for x in self._licenses}

    def find_from_classifier(self, classifier: str) -> Union[LicenseType,None]:
        return self.classifier_map.get(classifier)

    def find_from_license(self, license_line: str) -> Union[LicenseType,None]:
        for lt in self._licenses:
            for an in lt.alt_names:
                if an in license_line.casefold():
                    return lt
        return None


def get_metadata_line(line: str, metadata_prefix: str) -> Union[str,None]:
    if not line.startswith(metadata_prefix):
        return None
    return line[len(metadata_prefix)+1:].strip()


def get_license_str(license_classifier_list: list[LicenseType], license_line_list: list[LicenseType]) -> str:
    list_sep = ', '
    # Prefer classifier-based license strings
    license_str = list_sep.join([str(l) for l in license_classifier_list if not l.group])
    
    # Use license lines if no (specific) classifier license info
    if not license_str:
        license_str = list_sep.join([str(l) for l in license_line_list])

    # Allow group classifiers if nothing else is listed (e.g. :: OSI Approved)
    if not license_str:
        license_str = list_sep.join([str(l) for l in license_classifier_list])

    # Just print unknown otherwise
    if not license_str:
        license_str = 'Unknown'
    return license_str


def print_license_table(package_licenses: dict[str,tuple[str,str]]):
    pkg_header = 'Package'
    ver_header = 'Version'
    lic_header = 'License'

    pkg_len = max(len(pkg_header), max([len(k) for k in package_licenses.keys()]))
    ver_len = max(len(ver_header), max([len(v[0]) for v in package_licenses.values()]))
    
    logging.info(f'{pkg_header:<{pkg_len}} | {ver_header:<{ver_len}} | {lic_header}')
    logging.info(f'{"":-<{pkg_len}}-|-{"":-<{ver_len}}-|-{"":-<{len(lic_header)}}')
    for k,v in package_licenses.items():
        logging.info(f'{k:<{pkg_len}} | {v[0]:<{ver_len}} | {v[1]}')


def check_installed_licenses():
    workset = pkg_resources.working_set

    license_map = LicenseClassifierMap()

    package_licenses = dict[str,str]()
    for dist in workset:
        if not dist.has_metadata('METADATA'):
            continue

        license_classifier_list = list[LicenseType]()
        license_line_list = list[LicenseType]()
        for line in dist.get_metadata_lines('METADATA'):
            classifier = get_metadata_line(line, 'Classifier:')
            if classifier is not None:
                license_type = license_map.find_from_classifier(classifier)
                if license_type is None:
                    continue

                logging.debug(f'{dist.key} v{dist.version}: Classifier: {license_type.classifier_str()}')
                license_classifier_list.append(license_type)
                continue

            license_line = get_metadata_line(line, 'License:')
            if license_line is not None:
                license_type = license_map.find_from_license(license_line)
                if license_type is None:
                    continue

                logging.debug(f'{dist.key} v{dist.version}: License: {license_type}')
                license_line_list.append(license_type)
                continue

        license_str = get_license_str(license_classifier_list, license_line_list)
        package_licenses[dist.key] = (dist.version, license_str)

    package_licenses = dict[str,str](sorted(package_licenses.items()))
    print_license_table(package_licenses)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse requirements and relative to pkg_resources working set to determine')
    parser.add_argument('-v', '--verbose', action='count', dest='verbosity', default=0, help='Verbosity level (-v=info,-vv=debug)')

    args = parser.parse_args()

    # Forward all 
    log_modifier = min(10 * args.verbosity, 20)
    default_level = logging.WARNING
    log_level = default_level - log_modifier

    logging.basicConfig(level=log_level)
    check_installed_licenses()
