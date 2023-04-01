#! /usr/bin/python3 

"""sound.py"""

import evdev

def sound(child_conn2):

    while(True):

        soundValue = child_conn2.recv() 
        print('soundValue: ' + str(soundValue)) 

        if soundValue == 310:
            #subprocess.run(['mpg123', '-q -o alsa:hw:1,0 ./mp3/chew_roar.mp3'], universal_newlines=True)
            print(soundValue)

        if soundValue == 311:
            #subprocess.run(['mpg123', '-q -o alsa:hw:1,0 ./mp3/chew_roar.mp3'], universal_newlines=True)
            print(soundValue)
