import sounddevice as sd
import numpy as np
from pycaw.pycaw import AudioUtilities

sd.default.samplerate = 48000

#Example from PyCaw repo for audio control
class AudioController:
    def __init__(self, process_name):
        self.process_name = process_name
        self.volume = self.process_volume()

    def mute(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                interface.SetMute(1, None)
                print(self.process_name, "has been muted.")  # debug

    def unmute(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                interface.SetMute(0, None)
                print(self.process_name, "has been unmuted.")  # debug

    def process_volume(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                print("Volume:", interface.GetMasterVolume())  # debug
                return interface.GetMasterVolume()

    def set_volume(self, decibels):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                # only set volume in the range 0.0 to 1.0
                self.volume = min(1.0, max(0.0, decibels))
                interface.SetMasterVolume(self.volume, None)
                print("Volume set to", self.volume)  # debug

    def decrease_volume(self, decibels):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                # 0.0 is the min value, reduce by decibels
                self.volume = max(0.0, self.volume - decibels)
                interface.SetMasterVolume(self.volume, None)
                print("Volume reduced to", self.volume)  # debug

    def increase_volume(self, decibels):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                # 1.0 is the max value, raise by decibels
                self.volume = min(1.0, self.volume + decibels)
                interface.SetMasterVolume(self.volume, None)
                print("Volume raised to", self.volume)  # debug

loudSound = 0
decreases = 0

def print_sound(indata, outdata, frames, time, status):
    global loudSound, decreases
    volume_norm = np.linalg.norm(indata) * 10
    print(volume_norm)
    if volume_norm > 12.5: #adding a loud sound
        loudSound += 1
    if volume_norm < 5: #removing a loud sound
        if loudSound <= 0: #but not below 0
            loudSound = 0
            decreases = 0
        elif loudSound > 0:
            loudSound -= 1
    
    if loudSound == 0: #reset audio if loud noises stop
        for i in range(decreases*5):
            ac.increase_volume(.04/5)
        ac.set_volume(1)
        
    elif loudSound > 5: #gradually decrease volume if loud noises continue
        if decreases < 20:
            ac.decrease_volume(.04)
            decreases += 1

process = input("Enter the process name (without .exe): ")
process += ".exe"
ac = AudioController(process)
with sd.Stream(callback=print_sound):
    while True:
        sd.sleep(1000)