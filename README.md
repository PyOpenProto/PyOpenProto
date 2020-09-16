## PyOpenProto project

PyOpenProto project propose shareable, easy making and using softs and hardwares to play stimuli with high quality and timing accuracy.
The aim of this project is to contribute to standardise simple and efficient neuroscience protocol player solution (hardware + software) and make it accessible to a wide experiment context (from fundamental research to clinic).

This project is developped for instance to run experiments in neuroscience research. In this area, a high precision (ms) is needed between stimulation and recording equipement.  

For now, the existing solutions are :

## pyaudio_protocol
Pure python audio stimulation player coupled with parallel port syncronisation trigger. 
Two versions are available : one running on a regular computer (that has a LPT port, known as 'parralel port') and one with the StimulationBox harware solution we made, based on a RaspberryPi, as described below.
Pyaudio_protocol is used for audio experiment coupled with EEG recording. Uses a 'playframe' as the experiment guideline which is extern from the generique player engine.

## Stimulation box hardware
Pyaudio_protocol could be used with an open hardware stimulation box, easy to make and employ, inexpensive and allowing hight timming control and sound acuracy.
You can command a ready-to-use box to the Hemisphere company (bonjour@hemisphere-project.com) or do it yourself.
To creat a box you will need :
- raspberry pi 3 model B
- hifiberry DAC+ pro  
- to be continued..

