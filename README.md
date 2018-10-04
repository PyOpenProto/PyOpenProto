
The StimPunc project aims to propose shareable, easy making and using softs and hardwares to play stimuli with high quality and timing accuracy.

This project is developped for instance to run experiments in neuroscience research. In this area, a high precision (ms) is needed between stimulation and recording equipement.


For now, the existing solutions are :

## pyaudio_protocol & StimBox_v1
Pure python audio stimulation player coupled with parallel port syncronisation trigger. Used for audio experiment coupled with EEG recording. Uses a 'playframe' as the experiment guideline whch is extern from the generique player engine.
Could be used on a regular computer (that has a parralel port) or with the stimBox solution we made, based on a RaspberryPi. Associated stimBox documentation comming soon... 
