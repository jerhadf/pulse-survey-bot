from subprocess import Popen
import time
import sys
import os

filename = r"tests\pulse_surveys.py"
while True:
    os.system("taskkill /im chrome.exe /f")   
    print("\nStarting " + filename)
    p = Popen("python " + filename, shell=True)
    time.sleep(1)
    p.wait()