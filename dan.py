#! /usr/bin/python

import sys
import wave
import struct
import numpy
import os.path
import scipy.io.wavfile
import scipy.fftpack

def songLength(waveFile):
    return waveFile.getnframes()/float(waveFile.getframerate())

#ERROR CODE 1: Invalid command line
#ERROR CODE 2: Invalid file format
def throwError(code, arg):
    if code == 1:
        sys.stderr.write("ERROR: incorrect command line\n")
    if code == 2:
        sys.stderr.write("ERROR: " + arg + " is not a supported format\n")
    else:
        sys.stderr.write("ERROR: there was a problem")
    exit(code)

def getExtension(path):
    return os.path.splitext(path)[1]

def isValidExtension(path):
    extension = getExtension(path)
    extensions = [".wav"]
    return extension in extensions

def stereoToMono(byteVector):
    mono = [];
    for data in byteVector:
        average = (data[0] + data[1])/2.0
        mono.append(average)
    return mono

def isMatch(wavePath1, wavePath2):
    if not os.path.isfile(wavePath1) or not os.path.isfile(wavePath2):
        throwError(1, "")
    if not (isValidExtension(wavePath1)):
        throwError(2, wavePath1)
    if not (isValidExtension(wavePath2)):
        throwError(2, wavePath2)

    wave1 = wave.open(wavePath1, 'r')
    wave2 = wave.open(wavePath2, 'r')
 
    wave1_data = scipy.io.wavfile.read(wavePath1)[1]
    wave2_data = scipy.io.wavfile.read(wavePath2)[1]    
    
    wave1_data = wave1_data.astype(numpy.float)
    wave2_data = wave2_data.astype(numpy.float)
    
    wave1_mono = stereoToMono(wave1_data)
    wave2_mono = stereoToMono(wave2_data)

    chunkLength = 44100 * 4
    chunk = wave1_mono[0:chunkLength]
    
    print chunk
    
    if songLength(wave1) != songLength(wave2):
        return "NO MATCH"
    else:
        return "MATCH"
    
print isMatch(sys.argv[2], sys.argv[4])
#if sys.argv[1] != '-f' or sys.argv[3] != '-f':
#    print("Error incorrect syntax")
#    exit(1);
#else:	
#    waveFile = wave.open(sys.argv[2], 'r')
    
#    nchannels, sampwidth, framerate, nframes, comptype, compname =  waveFile.getparams()
#    print struct.unpack("HH", waveFile.readframes(1))
#    print songLength(nframes, framerate)
#for i in range(0,length):

        
