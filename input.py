import main
np = main.np
sd = main.sd
time = main.time

sd.default.samplerate = 48000

#Example from PyCaw repo for audio control

loudSound = 0
decreases = 0


def micVolume(indata, outdata, frames, time, status): #Changing volume of  process based on mic input
    global loudSound, decreases
    inNorm = np.linalg.norm(indata) * 10
    if inNorm > 10: #adding a loud sound
        loudSound += 1
    elif inNorm > 15: #adding a loud sound
        loudSound += 2
    elif inNorm > 20: #adding a loud sound
        loudSound += 3

    if inNorm < 5: #removing a loud sound
        if loudSound <= 0: #but not below 0
            loudSound = 0
            decreases = 0
        elif loudSound > 0:
            loudSound -= 1
    
    if loudSound == 0: #reset audio if loud noises stop
        main.reset()
    elif loudSound > 4: #gradually decrease volume if loud noises continue
        main.lower()