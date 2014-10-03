#! /usr/bin/python

import sys
import wave
import struct
import numpy
import os.path
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

def isMatch(wavePath1, wavePath2):
    if not os.path.isfile(wavePath1) or not os.path.isfile(wavePath2):
        throwError(1, "")
    if not (isValidExtension(wavePath1)):
        throwError(2, wavePath1)
    if not (isValidExtension(wavePath2)):
        throwError(2, wavePath2)

    wave1 = wave.open(wavePath1, 'r')
    wave2 = wave.open(wavePath2, 'r')
   
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

        
