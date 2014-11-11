#! /usr/bin/python

import unittest
import io
import sys
import contextlib
import subprocess

class MyTest(unittest.TestCase):
    
    def setUp(self):
        self.output = io.StringIO()
        self.saved_stdout = sys.stdout
        sys.stdout = self.output

    def tearDown(self):
        self.output.close()
        sys.stdout = self.saved_stdout

    def getResult(self, file1, file2):
        try:
            result = subprocess.check_output(["./dan", "-f", file1, "-f", file2])
            return result
        except subprocess.CalledProcessError, e:
            return e.output
    
    def getDirResult(self, dir1, dir2):
        try:
            result = subprocess.check_output(["./dan", "-d", dir1, "-d", dir2])
            return result
        except subprocess.CalledProcessError, e:
            return e.output
    
    #returns the formatted name of the file
    def formatFileName(self, path):
        tmp = []

        for i in range (0, len(path)):
            if path[i] == '/':
                tmp = []
            else:
                tmp.append(path[i])

        formatted_str = ''.join(tmp)
        return formatted_str

    def checkMatch(self, file1, file2):
        expected = "MATCH " + self.formatFileName(file1) + " " + self.formatFileName(file2) + "\n"
        self.assertEqual(self.getResult(file1, file2), expected) 

    def testA4Matches(self): 
        self.checkMatch("/course/cs4500f14/Assignments/A4/z01.wav", "/course/cs4500f14/Assignments/A4/bad0616.wav")
        self.checkMatch("/course/cs4500f14/Assignments/A4/z02.wav", "/course/cs4500f14/Assignments/A4/bad0616.wav")
        self.checkMatch("/course/cs4500f14/Assignments/A4/z03.wav", "/course/cs4500f14/Assignments/A4/bad2131.wav")
        self.checkMatch("/course/cs4500f14/Assignments/A4/z04.wav", "/course/cs4500f14/Assignments/A4/z03.wav")
        self.checkMatch("/course/cs4500f14/Assignments/A4/z05.wav", "/course/cs4500f14/Assignments/A4/Sor1929.wav")
        self.checkMatch("/course/cs4500f14/Assignments/A4/z06.wav", "/course/cs4500f14/Assignments/A4/Sor1929.wav")
        self.checkMatch("/course/cs4500f14/Assignments/A4/z07.wav", "/course/cs4500f14/Assignments/A4/Sor4959.wav")
        self.checkMatch("/course/cs4500f14/Assignments/A4/z08.wav", "/course/cs4500f14/Assignments/A4/z07.wav")
    
    def testA5Matches(self):
       expected = "MATCH curieuse.mp3 curieuse.wav\nMATCH curieuse2.wav curieuse.wav\nMATCH janacek.mp3 janacek2.wav\nMATCH maynard.wav maynard2.wav\nMATCH rimsky.mp3 rimsky2.wav\nMATCH sons2.wav sons.wav\nMATCH z03.wav z04.wav\nMATCH z07.wav z08.wav\n"  
       self.assertEqual(self.getDirResult("/course/cs4500f14/Assignments/A5/D1", "/course/cs4500f14/Assignments/A5/D2"), expected)
