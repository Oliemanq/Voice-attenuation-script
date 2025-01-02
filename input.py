import numpy as np 
from pycaw.pycaw import AudioUtilities #For audio control
import time
import main

sd.default.samplerate = 48000

#Example from PyCaw repo for audio control

loudSound = 0
decreases = 0


def micVolume(indata, outdata, frames, time, status): #Changing volume of  process based on mic input
    global loudSound, decreases
    volume_norm = np.linalg.norm(indata) * 10
    if volume_norm > 10: #adding a loud sound
        loudSound += 1
    elif volume_norm > 15: #adding a loud sound
        loudSound += 2
    elif volume_norm > 20: #adding a loud sound
        loudSound += 3
    print("Loud Sound:", loudSound) # debug

    if volume_norm < 5: #removing a loud sound
        if loudSound <= 0: #but not below 0
            loudSound = 0
            decreases = 0
        elif loudSound > 0:
            loudSound -= 1
    
    if loudSound == 0: #reset audio if loud noises stop
        main.reset()
        
    elif loudSound > 4: #gradually decrease volume if loud noises continue
        main.lower()

def outputVolume(indata, outdata, frames, time, status): #Changing volume of mic based on process input




def mainInput(process):
    global ac
    process += ".exe"
    if process == "cider.exe":
        process = "msedgewebview2.exe"

    ac = main.AudioController(process)
    with sd.Stream(callback=micVolume, callback=outputVolume):
        while True:
            sd.sleep(10000)

mainInput("cider")