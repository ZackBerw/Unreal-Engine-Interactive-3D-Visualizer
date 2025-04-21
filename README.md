# Unreal Engine Interactive 3D Visualizer
Here are some resources so you can get started with controlling events and effects inside of Unreal Engine 5.4 and above via an audio/MIDI to OSC workflow. This is achieved through some MaxForLive devices following an audio/MIDI to OSC protocol, as used in the Ableton Live Suite.

Features include a MIDI to OSC MaxForLive device that outputs data pretaining to Pitch Value, Velocity, Number of Notes being triggered, Time Between Notes, Duration, Random Number Generator, Scalable Counter, Current Bar Counter, Current Beat Counter, and Current Tempo.
There's also a flexible sample accurate MaxForLive Envelope Follower that allows you to generate float data based on the amplitude of incoming audio data.

A playlist of tutorials and walkthroughs regarding these MaxForLive devices and Unreal Engine blueprints can be found here:
https://www.youtube.com/playlist?list=PLBm2vQVHDfN3vJurr8QUmLK_y5LRKfunq

If you happen to have any ideas on how to improve the project, please feel free to contribute!

_______________________________________________________________________________________________________________________________________________________________________________________________________

Instructions:

- Download the files by clicking on the green button labelled "Code" then select the option that says "Download ZIP".
- To install the MaxForLive devices on Windows go to: Documents, Ableton, User Library, and then Presets. 
- From here you'll place the "MIDI to OSC" device in the "Max MIDI Effects" folder as found in the general "MIDI Effects" folder.
- The "Envelope to OSC" device will be placed in the "Max Audio Effects" folder as found within the general "Audio Effects" folder.
- For Mac repeat the same process, but instead go to Music, Ableton, User Library, Presets then repeat the process as outlined above.

- When it comes to the Unreal Engine side of things all you have to do is import or migrate the folder called "Reactive Visualizer" into the content folder of any Unreal project.

- Ensure that the "OSC (Open-Sound-Control) plugin is enabled so the OSC_Router bluepirnt works as intended. You can find this under: Edit, Plugins, OSC (Open-Sound-Control).
  
- To use the blueprints, start by placing the "Router" into any scene. This is what receives and parses the incoming OSC data as created by the MaxForLive devices or OSC/PAR. 
If you happen to be using a different setup and configuration for your Port and IP address, this is where you'll adjust those values. As the stock values are setup for working with one computer handling both the Ableton and Unreal Engine tasks simultaneously.

- Next import the "OSC Template" blueprint then connect it to the Router. This blueprint template is where you'll build all your events and effects. Just be sure that the Envelope Track Address, Macro Track Address, Macro Number, MIDI track address and MIDI trigger note values are correctly aligned with the MaxForLive devices and MIDI information being used in Ableton. 

- If you wish to control the camera and camera switching system import the "Camera Director" blueprint into the scene, select the router, and under the camera array choose the Cine Camera Actor that you have in your scene. This camera switching system allows for up to 12 different cameras to be used in one scene, as controlled by the MIDI data in Ableton. It specifically aligns with the 12 note values of C-2 through to C-1. The additional octave above that is what controls the look at targets and the octave above that adds camera shake if you so desire.

Here's a video walkthrough of the process:
https://www.youtube.com/watch?v=kIOKMqDuMMM
  
_______________________________________________________________________________________________________________________________________________________________________________________________________

The Unreal Engine blueprints and MaxForLive devices are built off of the work as found on the "Sem and Tris AV Club" as well as their own respective YouTube channels. So be sure to check out their channels for even further information on the basics regarding the blueprints. Thanks for allowing me to modify the project, as well as for allowing me to make the modified version open source.

Sem and Tris AV Club:
https://www.youtube.com/@semandtrisavclub4962

Sem Schreuder
https://www.youtube.com/@shimlaDnB

Tristan Gieler
https://www.youtube.com/@tristangieler
