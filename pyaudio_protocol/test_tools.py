# -*- coding: utf-8 -*-
import sounddevice as sd
import numpy as np
import time
import parallel

def list_audio_device():
    '''
    List audio devices
    Advice : select Alsa default mixer
    The audio_device number have to be given in core_gui.py corresponding to
    the one you wants to use on your computer
    '''
    print('Devices : ')
    print(sd.query_devices())


def show_device_sr(num_device=12):
    '''
    For a given device, test different sample rates to show those supported.
    '''
    # Sample rate to test:
    samplerates = 32000, 44100, 48000, 96000, 128000

    supported_samplerates = []
    for fs in samplerates:
        try:
            sd.check_output_settings(device=num_device, samplerate=fs)
        except Exception as e:
            print(fs, e)
        else:
            supported_samplerates.append(fs)
    print('Supported samplerates for device {:d}: '.format(num_device))
    print(supported_samplerates)


def get_sin(sr=44100, f_list=[1000], amp_list=[1], dur=1., dtype='float32'):
    '''
    Get a simple sinusoïde with
    sr          : sample rate (Hz)
    f_list      : frequencies (Hz)
    amp_list    : amplitudes
    dur         : duration (sec)
    dtype       : dtype
    '''
    assert len(f_list) == len(amp_list), "f_list and  amp_list must have the same dim"
    t = np.linspace(0.0, dur, dur*sr)
    y = 0

    for i, f in enumerate(f_list):
        y =  y + amp_list[i]*(np.sin(2.0*np.pi*f*t))

    y = y.astype(dtype)

    return y

def simple_test_stream():

    sr = 44100
    f_list = [1000, 500]
    amp_list = [1, 0.05]
    dur = 1.
    dtype = 'float32'
    sound_data = get_sin(sr, f_list, amp_list, dur, dtype)

    #Open audio stream with sound device
    start_time = time.time()
    stream = sd.OutputStream(device=num_device, samplerate=sr, channels=2, dtype=dtype)
    print("time to open a stream : %f seconds."%(time.time() - start_time))

    stream.start()
    stream.write(sound_data)
    stream.stop()
    stream.close()



def test_simple_syncro_parallel(num_device=12,  nb_stim=1000, trig_value=255):
    '''
    Test syncro between sound stream and parallel port over nb_stim trials.
    Need of course a parallel port.
    On linux need access to it. (ex /dev/parport0)
    '''

    #Get sound
    sr = 44100
    f_list = [1000]
    amp_list = [1]
    dur = 1.
    dtype = 'float32'
    sound_data = get_sin(sr, f_list, amp_list, dur, dtype)

    #Open audio stream with sound device
    start_time = time.time()
    stream = sd.OutputStream(device=num_device, samplerate=sr, channels=2, dtype=dtype)
    print("time to open a stream : %f seconds."%(time.time() - start_time))

    #Init parallel port
    p = parallel.Parallel()
    p.setData(0)

    #Start sending
    for i in range(nb_stim):
        stream.start()
        p.setData(trig_value) #parallel port could stay with this value - only a voltage change is view as a trigger
        stream.write(sound_data)
        stream.stop()
        p.setData(0)
        time.sleep(1) #s

    stream.close()
    time.sleep(5)


if __name__ == '__main__':

    list_audio_device()

    num_device = 12
    show_device_sr(num_device)

    nb_stim = 2
    trig_value = 255
    #test_simple_syncro_parallel(num_device, nb_stim, trig_value)

    simple_test_stream()
