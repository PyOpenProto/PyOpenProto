## PyOpenProto project

PyOpenProto project propose shareable, easy making and using softs and hardwares to play stimuli with high quality and timing accuracy.
The aim of this project is to contribute to standardise simple and efficient neuroscience protocol player solution (hardware + software) and make it accessible to a wide experiment context (from fundamental research to clinic).

This project is developped for instance to run experiments in neuroscience research. In this area, a high precision (ms) is needed between stimulation and recording equipement.  

For now, the existing solutions are :

## pyaudio_protocol
Pure python audio stimulation player coupled with parallel port syncronisation trigger (used for EEG synchronization in several EEG systems). 
Two versions are available : one running on a regular computer (that has a LPT port, known as 'parralel port') and one with the StimulationBox harware solution we made, based on a RaspberryPi, as described below.

Pyaudio_protocol is used for audio experiment coupled with EEG recording. It is based on a 'playframe' as the experiment guideline which is extern from the generique player engine. This playframe hosts stimuli sequence, timming information (ISI: Inter Stimulus Interval) and port code (0 to 255). See playframe_ex1.csv in the example section. The playframe is independant of the core reading process and could easily be changed, depending on the protocol/subject spécific order. External python code could be used to generate the coresponding playframe. Stimulus should be placed on a 'stim' folder and names should correspond to the one indicated in the plaframe.

Instalation on a computer: load or clone the git project, than run setup.py
You should have python 3 installed with numpy, pandas,and sounddevice packages and of course an LPT port (DB25, as known as parallel port). If you're computer is recent and does not have one, you can add an external PCI card that provide this port, on a tower computer. We do not recomand to use usb/LPT external device, as the timing acuracy could be damaged. 
Once it is intalled, you should provide your stimuli and playframe corresponding to your experiement and run 'py_proto_window.py'.

Installation the Stimulation Box's raspberry :
We provide a ready-to-use Raspbian install with all necessary configurations and codes. You just have to donwload the file (provided on Open Science Framework #todo: make it public), unzip and copy the image to your mini SD card.


## Stimulation box hardware
Pyaudio_protocol could be used with an open hardware stimulation box, easy to make and employ, inexpensive and allowing hight timming control and sound acuracy.
You can command a ready-to-use box to the Hemisphere company (bonjour@hemisphere-project.com) or do it yourself.
To creat a box you will need :
- raspberry pi 3 model B
- hifiberry DAC+ pro  
- 

