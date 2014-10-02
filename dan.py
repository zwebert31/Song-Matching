#! /usr/bin/python

import sys
import wave
import struct
import numpy
import os.path
def songLength(waveFile):
    return waveFile.getnframes()/float(waveFile.getframerate())

def isMatch(wavePath1, wavePath2):
    if not os.path.isfile(wavePath1) or not os.path.isfile(wavePath2):
        sys.stderr.write("ERROR\n")
        exit(1)

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

        
