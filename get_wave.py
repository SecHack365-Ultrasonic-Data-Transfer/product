# - coding: utf-8 -
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from scipy import signal
import pyaudio
import wave

import math
import parity_check

freq_std = 18000


#if __name__ == '__main__':
    #in_file = "hoge.wav"

def get_wave():    
    #data, rate = sf.read(in_file)
    
    in_code = ""
    in_txt = ""
    

    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 27
    WAVE_OUTPUT_FILENAME = "sample.wav"

    p = pyaudio.PyAudio()
    stream = p.open(
        format = FORMAT,
        channels = CHANNELS,
        rate = RATE,
        input = True,
        frames_per_buffer = chunk
    )

    all = []
    for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
        data = stream.read(chunk)
        all.append(data)
        try:
            print(int(i / 50))
            pass
        except ZeroDivisionError as identifier:
            pass

    stream.close()
    p.terminate()
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(p.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(all))
    waveFile.close()

    in_file = WAVE_OUTPUT_FILENAME

    data, rate = sf.read(in_file)

    #data = b''.join(all)
    in_sec = len(data) / RATE
    for i in range(int(in_sec)):
        X = fftpack.fft(data[i*44100:(i+1)*44100])
        freqList = fftpack.fftfreq(44100, d=1.0/ RATE)
        
        amplitude = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X]
        in_freq = amplitude.index(max(amplitude))  #1番大きい振幅を拾ってるだけ(雑音出たら、たぶん上手くいかない)
        
        for j in range(16):
            l_lim = ((freq_std + 100*(j-1))+(freq_std + 100* j))/2
            h_lim = ((freq_std + 100*(j+1))+(freq_std + 100*j))/2
            if (in_freq > l_lim )and(in_freq < h_lim):
                in_code += hex(j)[2:4]
                break
        print(i, in_freq, j)

        plt.show()
    in_txt,parity_flg = parity_check.parity_checker(in_code)
    #for code in range(int(in_sec/2)):
    #    in_txt += chr(int(in_code[code*2:(code+1)*2], 16))
    print("input : ", in_code, "→", in_txt)
    #print(in_code[code*2:(code+1)*2], chr(int(in_code[code*2:(code+1)*2], 16)))