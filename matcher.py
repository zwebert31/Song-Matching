#! /usr/bin/python

import sys
import wave
if sys.argv[1] != '-f' or sys.argv[3] != '-f':
    print("Error incorrect syntax");
    exit(1);
else:	
    print(sys.argv[2]);
