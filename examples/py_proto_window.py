

from PyQt4 import QtGui
import pandas as pd
import random
import numpy as np

import pyaudio_protocol as pap

class PyProto_Window(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.gridlayout = QtGui.QGridLayout()
        self.setLayout(self.gridlayout)

        self.but_start = QtGui.QPushButton('Start')
        self.gridlayout.addWidget(self.but_start)
        self.but_start.clicked.connect(self.start)
        self.but_start.setEnabled(True)

        self.but_stop = QtGui.QPushButton('Stop')
        self.gridlayout.addWidget(self.but_stop)
        self.but_stop.clicked.connect(self.stop)
        self.but_stop.setEnabled(False)

    def initialize(self):
        self.proto = pap.PyAudio_protocol()
        self.proto.ThreadSoundTrig.signals.end_playframe.connect(self.close)

    def set_params(self, playframe, num_device, stim_folder):
        self.playframe = playframe
        self.num_device = num_device
        self.stim_folder = stim_folder
        self.proto.set_config(self.playframe, self.num_device, self.stim_folder)

    def start(self):
        self.proto.start()
        self.but_start.setEnabled(False)
        self.but_stop.setEnabled(True)

    def stop(self):
        self.proto.stop()
        self.but_start.setEnabled(False)
        self.but_stop.setEnabled(False)

    def get_signal(self, sig):
        print('signal : ', sig)

def test_PyProto_Window():

    app = QtGui.QApplication([])

    #Params :
    playframe_csv = 'playframe_ex1.csv'
    playframe = pd.read_csv(playframe_csv)
    num_device = 12
    stim_folder = './stims_ex/'

    proto_win = PyProto_Window()
    proto_win.initialize()
    proto_win.set_params(playframe, num_device, stim_folder)
    proto_win.show()

    app.exec_()



if __name__ == '__main__':
    test_PyProto_Window()
