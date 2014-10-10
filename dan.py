#! /usr/bin/python

import sys
import wave
import struct
import numpy
import os.path
import scipy.io.wavfile
import scipy.fftpack

DEBUG = 0

#Returns the length of the song in seconds
def songLength(waveFile):
    return waveFile.getnframes()/float(waveFile.getframerate())

#ERROR CODE 1: Invalid command line
#ERROR CODE 2: Invalid file format
def throwError(code, arg):
    if code == 1:
        sys.stderr.write("ERROR: incorrect command line\n")
    if code == 2:
        sys.stderr.write("ERROR: " + formatFileName(arg)
                         + " is not a supported format\n")
    else:
        sys.stderr.write("ERROR: there was a problem")
    exit(code)

#returns the extension of the file
def getExtension(path):
    return os.path.splitext(path)[1]

#returns 1 if extension is valid, 0 if invalid
def isValidExtension(path):
    extension = getExtension(path)
    extensions = [".wav"]
    return extension in extensions

#returns the name of the file
def formatFileName(path):
    tmp = []

    for i in range (0, len(path)):
        if path[i] == '/':
           tmp = []
        else:
           tmp.append(path[i])

    formatted_str = ''.join(tmp)
    return formatted_str

#convert a stereo byte vector to a mono signal
def stereoToMono(byteVector):
    mono = [];
    for data in byteVector:
        average = (data[0] + data[1])/2.0
        mono.append(average)
    return mono

#returns 1 if frequencies are a match, 0 if they are not
def compareFreq(freq1, freq2, maxKeys):
    keyIndex1 = 0;
    keyIndex2 = 0;
    for i in range(1,len(freq1)/2):
        if(freq1[i] > freq1[keyIndex1]): 
            keyIndex1 = i
        
        if(freq2[i] > freq2[keyIndex2]): 
            keyIndex2 = i
        
        #print str(freq1[i]) + " VS " + str(freq2[i])
    if (keyIndex1 == keyIndex2):
        return 1;
    else:
        return 0; 

#returns a list of magnitudes from an fftArray
def calculateMagnitude(fftArray):
    magArray = []
    for i in range (0, len(fftArray)):
        magArray.append(numpy.sqrt(numpy.power(fftArray[i][0], 2) + numpy.power(fftArray[i][1], 2)))
    return magArray

#returns MATCH if two songs match, NO MATCH if two songs do not match
def isMatch(wavePath1, wavePath2):
    if not os.path.isfile(wavePath1) or not os.path.isfile(wavePath2):
        throwError(1, "")
    if not (isValidExtension(wavePath1)):
        throwError(2, wavePath1)
    if not (isValidExtension(wavePath2)):
        throwError(2, wavePath2)

    #open up the files, make sure they are valid wav files
    try:
        wave1 = wave.open(wavePath1, 'r')
    except wave.Error:
        throwError(2, wavePath1)

    try:
        wave2 = wave.open(wavePath2, 'r')
    except wave.Error:
        throwError(2, wavePath2)

    wave1_results = scipy.io.wavfile.read(wavePath1)
    wave2_results = scipy.io.wavfile.read(wavePath2)

    wave1_data = wave1_results[1]
    wave2_data = wave2_results[1]
    
    wave1_numSamples = len(wave1_data)
    wave1_samplingRate = wave1_results[0]
    
    wave2_numSamples = len(wave2_data)
    wave2_samplingRate = wave2_results[0]    

    wave1_data = wave1_data.astype(numpy.float)
    wave2_data = wave2_data.astype(numpy.float)
    
    wave1_mono = stereoToMono(wave1_data)
    wave2_mono = stereoToMono(wave2_data)

    # set chunk size to one second
    chunkSize = 44100
    
    matchCount = 0 #number of chunk matches

    #iterate through chunks, perform fft and compare the chunks
    for i in range (0, wave1_numSamples / chunkSize):
        
        startBounds = i * chunkSize

        endBounds = (i + 1) * chunkSize
        
	#print "starting fft"

	#fft for wav1
        fftResult1 = numpy.fft.fft(wave1_data[startBounds:endBounds])
        
        #fft for wav2
        fftResult2 = numpy.fft.fft(wave2_data[startBounds:endBounds])
        
        #calculate the magnitudes
        mag1 = calculateMagnitude(fftResult1)
        mag2 = calculateMagnitude(fftResult2)
        
        #compare magnitudes
        if compareFreq(mag1, mag2, 1) == 1:
            matchCount += 1
  
    if songLength(wave1) != songLength(wave2):
        return "NO MATCH"
    else:
        if matchCount > (wave1_numSamples / chunkSize / 2):
            return "MATCH " + formatFileName(wavePath1) + " " + formatFileName(wavePath2)
        else:
            return "NO MATCH"

#make sure user has put in correct input
if sys.argv[1] != '-f' or sys.argv[3] != '-f':
     throwError(1, "")

print isMatch(sys.argv[2], sys.argv[4])

#    nchannels, sampwidth, framerate, nframes, comptype, compname =  waveFile.getparams()
#    print struct.unpack("HH", waveFile.readframes(1))
#    print songLength(nframes, framerate)        
