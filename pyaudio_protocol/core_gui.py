import os
from PyQt5 import QtCore
from PyQt5.Qt import QMutex
import soundfile as sf
import sounddevice as sd
import parallel
import time


def play_sound_and_trig(stream, sound_data, p_port, trig_value, isi):
    stream.start()
    p_port.setData(trig_value)
    #print('sound_data : ', sound_data)
    stream.write(sound_data)
    stream.stop()
    p_port.setData(0)
    time.sleep(isi)
    #a trigger is view when there is a voltage change
    #on the parallel port, so no need to reset it now.


class Signals(QtCore.QObject):
    start_stim = QtCore.pyqtSignal()
    end_stim = QtCore.pyqtSignal()
    end_playframe = QtCore.pyqtSignal()

class Qt_sound_trig(QtCore.QThread):
    '''
    On joue le son dans un stream unique pour la Classe
    via un thread car la methode write est blockante
    (enfin suivant le device/backend choisi)
    '''
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.signals = Signals()
        self.mutex = QMutex()
        self.running = False
        self.current = 0

    def set_params(self, playframe, stream, p_port, stim_folder, dtype):
        self.playframe = playframe
        self.stream = stream
        self.p_port = p_port
        self.stim_folder = stim_folder
        self.sound_dtype = dtype

    def run(self):
        self.mutex.lock()
        self.running = True
        self.mutex.unlock()

        for index, row in self.playframe.iterrows():   #playframe.iloc[self.current:]
            self.mutex.lock()
            if not self.running:
                self.current = index
                print('Stopped at index ' + str(self.current))
                self.mutex.unlock()
                break
            self.mutex.unlock()
            print('index : ', index)
            sound_data, sample_rate = sf.read(self.stim_folder + row['Stimulus'] + '.wav')
            sound_data = sound_data.astype(self.sound_dtype) #TODO why sounds are in float64 ??
            trig_value = row['Trigger']
            isi = round(row['ISI'] * 10**-3, 3)
            print('isi : ', isi)
            print('Reading {}'.format(row['Stimulus']))
            self.signals.start_stim.emit()
            play_sound_and_trig(self.stream, sound_data, self.p_port, trig_value, isi)
            self.signals.end_stim.emit()

        self.signals.end_playframe.emit()

    def stop(self):
        self.mutex.lock()
        self.running = False
        self.mutex.unlock()

#TODO : QObjet avec Qtimer qui s'autolance


class PyAudio_protocol():
    def __init__(self, parent = None):
        self.p_port = parallel.Parallel()
        self.p_port.setData(0)
        self.ThreadSoundTrig = Qt_sound_trig()
        self.state = 'Init'
        print('self.state : ', self.state)

    def set_config(self, playframe, num_device, stim_folder, sample_rate=44100, channels=2, dtype='float32'):
        self.playframe = playframe
        self.num_device = num_device
        self.stim_folder = stim_folder
        self.sample_rate = sample_rate
        self.channels = channels
        self.stream = sd.OutputStream(device = num_device,
            samplerate = sample_rate, channels=channels, dtype=dtype)
        self.ThreadSoundTrig.set_params(playframe, self.stream, self.p_port, stim_folder, dtype)
        self.state = 'Config'
        print('self.state : ', self.state)

    def start(self):
        self.ThreadSoundTrig.start()
        self.state = 'Running : stim %i %s'.format('trucTODO')
        print(self.state)

    def pause(self):
        #TODO
        pass

    def stop(self):
        self.ThreadSoundTrig.stop()
        self.state = 'Stopped on stim  %i %s'.format('trucTODO')

    def closeEvent(self, event):
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
        from PyQt5 import QtWidgets
        import pandas as pd

        app = QtWidgets.QApplication([])
        proto = PyAudio_protocol()

        num_device = 12
        playframe_csv = './../examples/playframe_ex1.csv'
        playframe = pd.read_csv(playframe_csv)
        stim_folder = './../examples/stims_ex/'

        proto.set_config(playframe=playframe, num_device=num_device, stim_folder=stim_folder)
        proto.start()

        def close():
            proto.stop()
            app.quit()

        proto.ThreadSoundTrig.signals.end_playframe.connect(close)

        app.exec_()


if __name__ == '__main__':

    test_audioproto()
