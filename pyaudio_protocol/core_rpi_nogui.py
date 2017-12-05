import os
import soundfile as sf
import sounddevice as sd
import time

import RPi.GPIO as GPIO
import numpy as np
from threading import Thread, Lock
from subprocess import call


def play_sound_and_trig_rpi(stream, sound_data, GPIO_trigOn, isi):
    stream.start()
    GPIO.output(GPIO_trigOn,1)
    stream.write(sound_data)
    stream.stop()
    GPIO.output(GPIO_trigOn, 0)
    time.sleep(isi)
    #a trigger is view when there is a voltage change
    #on the parallel port, so no need to reset it fast.

def get_GPIO_bool(trig_value, parralel_GPIO):
    bool_filter = np.array(np.array(list('{0:08b}'.format(trig_value))), dtype=bool)
    GPIO_trigOn = parralel_GPIO[bool_filter].tolist()
    print(GPIO_trigOn)
    print(type(GPIO_trigOn))
    return GPIO_trigOn


class sound_trig_Thread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.lock = Lock()
        self._running = False
        self.current = 0

    def set_params(self, playframe, stream, stim_folder, sound_dtype,
                parralel_GPIO, LEDState_GPIO):
        self.playframe = playframe
        self.stream = stream
        self.stim_folder = stim_folder
        self.sound_dtype = sound_dtype

        self.parralel_GPIO = parralel_GPIO
        for i in self.parralel_GPIO:
            GPIO.setup(i.item(), GPIO.OUT)
            GPIO.output(i.item(), GPIO.LOW)

        self.LEDState_GPIO = LEDState_GPIO

    def running(self):
        with self.lock:
            return self._running

    def run(self):
        with self.lock:
            self._running = True

        nb_items = self.playframe.shape[0]
        GPIO.output(self.LEDState_GPIO[0], GPIO.HIGH)
        Led1 = 0
        Led2 = 0
        Led3 = 0

        for index, row in self.playframe.iterrows():   #playframe.iloc[self.current:]
            if not self.running():
                self.current = index
                print('Stopped at index ' + str(self.current))
                break

            if index > round(nb_items/4) and Led1 == 0:
                GPIO.output(self.LEDState_GPIO[1], GPIO.HIGH)
                Led1 = 1
            if index > round(nb_items/2) and Led2 == 0:
                GPIO.output(self.LEDState_GPIO[2], GPIO.HIGH)
                Led2 = 1
            if index > 3*round(nb_items/4 and Led3 == 0):
                GPIO.output(self.LEDState_GPIO[3], GPIO.HIGH)
                Led3 = 1

            print('index : ', index)
            sound_data, sample_rate = sf.read(self.stim_folder + row['Stimulus'] + '.wav')
            sound_data = sound_data.astype(self.sound_dtype) #TODO why sounds are in float64 ??
            trig_value = row['Trigger']
            GPIO_trigOn = get_GPIO_bool(trig_value, self.parralel_GPIO)
            isi = round(row['ISI'] * 10**-3, 3)
            print('isi : ', isi)
            print('Reading {}'.format(row['Stimulus']))

            #play_sound_and_trig_rpi(self.stream, sound_data, GPIO_trigOn, isi)
            try:
                self.stream.start()
                GPIO.output(GPIO_trigOn,1)
                self.stream.write(sound_data)
                self.stream.stop()
                GPIO.output(GPIO_trigOn, 0)
                time.sleep(isi)
            except ValueError:
                print(ValueError)

        GPIO.output(self.LEDState_GPIO[4], GPIO.HIGH)

    def stop(self):
        with self.lock:
            self._running = False
        #rais sd.CallbackAbord() ??
        self.stream.abort()


#TODO LOG
#TODO graph d'etat
class PyAudio_protocol_rpi():

    _config_GPIO = { 'mode':0,  #0 BOARD 1 BCM
            'parralel':np.array([29,31,33,16,37,36,18,32], dtype=np.int32),
            #'parralel':np.array([29,31,33,35,37,36,38,40], dtype=np.int32)    #basic rpi
            'butStart':7,
            'butStop':11,
            'LED_Start':22,
            'LED_State':[13,15,19,21,23]
    }

    def __init__(self, parent = None):
        GPIO.setmode(GPIO.BOARD)
        #self.gpio_Button_Thread = gpio_Button_Thread()
        self.sound_trig_Thread = sound_trig_Thread()
        self._running = False
        self._playing = False
        self.state = 'Init'
        print('self.state : ', self.state)

    def set_config(self, playframe, num_device=5, stim_folder='', sample_rate=44100,
            channels=2, sound_dtype='float32'):
        '''
        '''
        self.playframe = playframe
        self.num_device = num_device
        self.stim_folder = stim_folder
        self.sample_rate = sample_rate
        self.channels = channels
        self.sound_dtype = sound_dtype
        self.stream = sd.OutputStream(device = num_device,
            samplerate = sample_rate, channels=channels, dtype=sound_dtype)

        if self._config_GPIO['mode'] == 0:
            GPIO.setmode(GPIO.BOARD)
        else:
            GPIO.setmode(GPIO.BCM)
        #GPIO.setwarnings(False)

        self.parralel_GPIO = self._config_GPIO['parralel']
        self.butStart_GPIO = self._config_GPIO['butStart']
        self.butStop_GPIO = self._config_GPIO['butStop']
        #self.LEDStart_GPIO = self._config_GPIO['LED_Start']
        self.LEDState_GPIO = self._config_GPIO['LED_State']

        self.sound_trig_Thread.set_params(self.playframe,
            self.stream, self.stim_folder, self.sound_dtype, self.parralel_GPIO,
            self.LEDState_GPIO)

        GPIO.setup(self.butStart_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.butStop_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self._config_GPIO['LED_Start'],GPIO.OUT)
        [GPIO.setup(ii,GPIO.OUT) for ii in self._config_GPIO['LED_State']]

        self.state = 'Config'
        print('self.state : ', self.state)

    def running(self):
        return self._running #do we need a mutex ?

    def playing(self):
        return self._playing #do we need a mutex ?

    def onStartButton(self, numGPIO):
        print('press start')
        if not self.playing():
            print('started')
            self.sound_trig_Thread.start()
            self._playing = True


    def onStopButton(self, numGPIO):
        print('Stopped')
        self.stop()


    def start(self):
        GPIO.add_event_detect(self.butStart_GPIO, GPIO.RISING)
        GPIO.add_event_detect(self.butStop_GPIO, GPIO.RISING)
        GPIO.add_event_callback(self.butStart_GPIO, self.onStartButton)
        GPIO.add_event_callback(self.butStop_GPIO, self.onStopButton)

        self.state = 'Running : stim %i %s'.format('trucTODO')
        self._running = True
        print(self.state)
        GPIO.output(self._config_GPIO['LED_Start'],GPIO.HIGH)
        while self.running():
            time.sleep(0.5)

    def pause(self):
        #TODO
        pass

    def stop(self):
        '''
        In this case, we want stop button stops all the process and shutdown the rpi
        '''
        GPIO.remove_event_detect(self.butStart_GPIO)
        GPIO.remove_event_detect(self.butStop_GPIO)
        GPIO.output(self._config_GPIO['LED_Start'],GPIO.LOW)
        self._running = False

        if self.playing():
            self.sound_trig_Thread.stop()
            self._playing = False
            [GPIO.output(ii,GPIO.LOW) for ii in self._config_GPIO['LED_State']]

        #self.state = 'Stopped on stim  %i %s'.format('trucTODO')
        self.stream.close()
        #time.sleep(2)

        #switch off the rpi
        #call("sudo shutdown -h now", shell=True)

    def get_state(self):
        return self.state

    def save_results(self):
        #TODO
        pass



def test_audioproto():
        '''
        Test with playframe and stims given in examples folder.
        Should be run from core_rpi_nogui.py folder
        '''
        import pandas as pd

        proto = PyAudio_protocol()

        num_device = 2
        playframe_csv = './../examples/playframe_ex1.csv'
        playframe = pd.read_csv(playframe_csv)
        stim_folder = './../examples/stims_ex/'
        sample_rate = 44100
        channels = 2
        sound_dtype='float32'

        proto.set_config(playframe, num_device, stim_folder, sample_rate, channels,
            sound_dtype)
        proto.start()



if __name__ == '__main__':

    test_audioproto()
