
This project aims to propose flexible soft and hardware to run experiments that needs a high timing acuraty to synchronise different equipments.
For example, we developp this project for neuroscience research to get the best synchonisation between the presentation of audio stimuli with cerebral activity recording (EEG). This kind of experiment needs to be at milisec precision.

For now, the existing solutions are :

## pyaudio_protocol
Pure python audio stimulation coupled with parallel port syncronisation trigger. Could be used on a regular computer (that has a parralel port) or with the stimBox solution we made, based on a RaspberryPi. Please find the stimBox documentation here (comming soon). 
