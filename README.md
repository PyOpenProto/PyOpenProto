## PyOpenProto project

PyOpenProto project propose shareable, easy making and using softs and hardware to play stimuli with high quality and timing accuracy.
The aim of this project is to contribute to standardize simple and efficient neuroscience protocol player solution (hardware + software) and make it accessible to a wide experiment context (from fundamental research to clinic).

This project is developed for instance to run experiments in neuroscience research. In this area, a high precision (ms) is needed between stimulation and recording equipment.  

For now, the existing solutions are : pyaudio_protocol.

## pyaudio_protocol
Pyaudio protocol is a pure python audio stimulation player coupled with parallel port synchronization trigger (used for EEG synchronization in several EEG systems).
Two versions are available : one running on a regular computer (that has a LPT port, known as 'parallel port') and one with the StimulationBox hardware solution we made, based on a Raspberry Pi, as described below.

Pyaudio_protocol is used for audio experiment coupled with EEG recording. It is based on a 'playframe' as the experiment guideline which is extern from the generique player engine. This playframe hosts stimuli sequence, timing information (ISI: Inter Stimulus Interval) and port code (0 to 255). See "playframe_ex1.csv" in  example section. The playframe is independent of the core reading process and could easily be changed, depending on the protocol/subject specific order. External python code could be used to generate the corresponding playframe as illustrated by "playframe_generation_example.py" in playframe_generation_example section. Stimulus should be placed on a 'stim' folder and names should correspond to the one indicated in the playframe. (path to playframe and stimuli folder could be changed inside the code if needed)

**Installation on a classic computer**: load or clone the git project, than run setup.py
You should have python 3 installed with numpy, pandas, and sounddevice packages and of course an LPT port (DB25, as known as parallel port). If your computer is recent and does not have one, you can add an external PCI card that provide this port, on a tower computer. We do not recommend to use USB/LPT external device, as the timing accuracy could be damaged.
Once it is installed, you should provide your stimuli and playframe corresponding to your experiment and run 'py_proto_window.py'.

**Installation on the Stimulation Box's Raspberry** :
We provide a ready-to-use Raspbian install with all necessary configurations and codes. You just have to download the file (provided on Open Science Framework #todo: make it public), unzip and copy the image to your mini SD card.


## Stimulation box hardware
Pyaudio_protocol could be used with an open hardware stimulation box, easy to make and employ, inexpensive and allowing high timing control and sound accuracy.
You can command a ready-to-use box to the Hemisphere company (bonjour@hemisphere-project.com) or do it yourself.
To creat a box you will need :
- raspberry pi 3 model B (+ loader)
- hifiberry DAC+ pro (+ hosting box)
- Mini SD card (15gb)
- DB25 female port
- usb battery
- 6 LED, resistances, wires, on/off button, start button
- usb keys

More information about 'how to' construct your own box will be given soon here and in open behavior website. https://edspace.american.edu/openbehavior/
You can find a ready to use Raspbian operating system for your box with all configurations and code included on Open Science Framework https://osf.io/3muqk/
