import os
import soundfile as sf
import sounddevice as sd
import parallel
import time

import RPi.GPIO as GPIO
import numpy as np
from threading import Thread, Lock


def play_sound_and_trig_rpi(stream, sound_data, GPIO_to_active, isi):
    stream.start()
    GPIO.output(GPIO_to_active,1)
    stream.write(sound_data)
    stream.stop()
    GPIO.output(GPIO_to_active, 0)
    time.sleep(isi)
    #a trigger is view when there is a voltage change
    #on the parallel port, so no need to reset it fast.

def get_GPIO_bool(trig_value):
    bool_filter = np.array(np.array(list('{0:08b}'.format(trig_value))), dtype=bool)
    GPIO_to_active = used_GPIO[bool_filter].tolist()
    print(GPIO_to_active)
    print(type(GPIO_to_active))
    return GPIO_to_active


class sound_trig_Thread(Thread):
    def __init__(self):
        Thread.__init__(self, running)
        self.mutex = Lock()
        self._running = False
        self.current = 0

    def set_params(self, playframe, stream, p_port, stim_folder, dtype):
        self.playframe = playframe
        self.stream = stream
        self.p_port = p_port
        self.stim_folder = stim_folder
        self.sound_dtype = dtype

    def running(self):
        with self.lock:
            return self._running

    def run(self):
        with mutex:
            self.running = True

        for index, row in self.playframe.iterrows():   #playframe.iloc[self.current:]
            with mutex:
                if not self.running:
                    self.current = index
                    print('Stopped at index ' + str(self.current))
                    break

            print('index : ', index)
            sound_data, sample_rate = sf.read(self.stim_folder + row['Stimulus'] + '.wav')
            sound_data = sound_data.astype(self.sound_dtype) #TODO why sounds are in float64 ??
            trig_value = row['Trigger']
            GPIO_to_active = get_GPIO_bool(trig_value)
            isi = round(row['ISI'] * 10**-3, 3)
            print('isi : ', isi)
            print('Reading {}'.format(row['Stimulus']))
            play_sound_and_trig_rpi(self.stream, sound_data, self.p_port, trig_value, isi)

    def stop(self):
        with mutex:
            self._running = False


class gpio_Button_Thread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.lock = Lock()
        self._running = False
        self.ThreadSoundTrig = sound_trig_Thread()

    def running(self):
        with self.lock:
            return self._running

    def run(self):
        #if button start cliked, onStartButton
        #if button stop cliked, onStopButton

    def onStartButton(self):
        if not self.running():
            self.sound_trig_Thread.start()
            self._running = True

    def onStopButton(self):
        if self.running():
            self.sound_trig_Thread.start()
            self._running = True

    def stop(self):
        with mutex:
            self._running = False


#TODO LOG
#TODO graph d'etat
class PyAudio_protocol_rpi():
    def __init__(self, parent = None):
        #self.ThreadSoundTrig = sound_trig_Thread()
        self.gpio_Button_Thread = Qt_sound_trig()
        GPIO.setmode(GPIO.BOARD)
        #self.used_GPIO = np.array([29,31,33,35,37,36,38,40], dtype=np.int32)    #basic rpi
        self.used_GPIO = np.array([29,31,33,16,37,36,18,32], dtype=np.int32)     #hiffiBerry
        for i in self.used_GPIO:
            GPIO.setup(i.item(), GPIO.OUT)
            GPIO.output(i.item(), GPIO.LOW)
        self.state = 'Init'
        print('self.state : ', self.state)

    def set_config(self, playframe, num_device=3, stim_folder='', sample_rate=44100, channels=2, dtype='float32'):
        self.playframe = playframe
        self.num_device = num_device
        self.stim_folder = stim_folder
        self.sample_rate = sample_rate
        self.channels = channels
        self.stream = sd.OutputStream(device = num_device,
            samplerate = sample_rate, channels=channels, dtype=dtype)
        self.state = 'Config'
        print('self.state : ', self.state)

    def start(self):
        self.gpio_Button_Thread.start()
        self.state = 'Running : stim %i %s'.format('trucTODO')
        print(self.state)

    def pause(self):
        #TODO
        pass

    def stop(self):
        self.ThreadSoundTrig.stop()
        self.state = 'Stopped on stim  %i %s'.format('trucTODO')
        self.stream.close()

    def get_state(self):
        return self.state

    def save_results(self):
        #TODO
        pass



def test_audioproto():
        '''
        Test with playframe and stims given in examples folder.
        Should be run from core.py folder
        '''
        import pandas as pd

        proto = PyAudio_protocol()

        num_device = 12
        playframe_csv = './../examples/playframe_ex1.csv'
        playframe = pd.read_csv(playframe_csv)
        stim_folder = './../examples/stims_ex/'

        proto.set_config(playframe=playframe, num_device=num_device, stim_folder=stim_folder)
        proto.start()



if __name__ == '__main__':

    test_audioproto()
