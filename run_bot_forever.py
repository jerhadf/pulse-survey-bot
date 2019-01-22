#!/usr/bin/python
from subprocess import Popen
import time
import sys

filename = r"tests\pulse_surveys.py"
while True:
    print("\nStarting " + filename)
    p = Popen("python " + filename, shell=True)
    time.sleep(1)
    p.wait()