#! /usr/bin/python3

#Mel Dundas
#Mar 21, 2020
#melbotpi5-l298.py

#add bluedot phone control
#Dec 29, 2020

#changed to Android WiFi phone control
#Feb 15, 2021

#change pinouts to account for TFT
#Feb 02, 2022

#Change pinouts to match the Motor Controller
#Added some PWM readings from phone.py to control the speed of the bot
#Comment out the printing to console because we run this from systemd
#Mar 30, 2023


import pigpio
import time
from multiprocessing import Process, Pipe
import phone
import sound

import multiprocessing as mp
#print("Number of processors: ", mp.cpu_count())

"""
So we send the PWM signal to the PWM channel
One of the IN Pins high and the other low is what does the direction
Swap the HIGH and LOW to change the direction

These are the original pinout
my left and right track were backwards
PWML = 12
IN1L = 5 
IN2L = 6 
PWMR = 13
IN3R = 22 
IN4R = 27
"""

PWML = 13
IN1L = 22
IN2L = 27
PWMR = 12
IN3R = 5
IN4R = 6

# Defining main function
def main():
    
    #init motors off
    pi.write(IN1L,0)
    pi.write(IN2L,0)
    pi.write(IN3R,0)
    pi.write(IN4R,0)

    #set pins output
    pi.set_mode( IN1L, pigpio.OUTPUT)
    pi.set_mode( IN2L, pigpio.OUTPUT)
    pi.set_mode( IN3R, pigpio.OUTPUT)
    pi.set_mode( IN4R, pigpio.OUTPUT)
    pi.set_mode( PWML, pigpio.OUTPUT)
    pi.set_mode( PWMR, pigpio.OUTPUT)

    #left track
    pi.set_PWM_frequency(PWML,8000)
    pi.set_PWM_range(PWML, 100)
    pi.set_PWM_dutycycle(PWML,   0) # PWM off

    #right track
    pi.set_PWM_frequency(PWMR,8000)
    pi.set_PWM_range(PWMR, 100)
    pi.set_PWM_dutycycle(PWMR,   0) # PWM off

    while(True):

        gamepadValues = parent_conn.recv()
#        print('gamepadValues: ' + gamepadValues[0] + ' ' + str(gamepadValues[1]) + ' ' + gamepadValues[2]+ ' ' + str(gamepadValues[3])+ ' ' + gamepadValues[4])


        """
        gampadValues 
        from phone.py
        [ mydict['LDir'], mydict['LLen'], mydict['RDir'], mydict['RLen'], mydict['But'] ]
        0 = LDir F or B
        1 = LLen 0 - 100
        2 = RDir F or B
        3 = RLen 0 - 100
        4 = But X or Y
        """    
        
        #define the PWM variables
        # I need to do this or the program complains when its run
        leftPWM = 0
        rightPWM = 0

        #gamepad control for left and right sticks
        try:
            leftJoyValue = int(gamepadValues[1])
            rightJoyValue = int(gamepadValues[3])
        except ValueError:
            print("Invalid joystick value: ", gamepadValues[1], gamepadValues[3])
        else:
            if leftJoyValue != 0:
                if gamepadValues[0] == 'F':
                    leftPWM = (leftJoyValue)
                    pi.write(IN1L, 0)
                    pi.write(IN2L, 1)
                elif gamepadValues[0] == 'B':
                    leftPWM = (leftJoyValue)
                    pi.write(IN1L, 1)
                    pi.write(IN2L, 0)

            if rightJoyValue != 0:
                if gamepadValues[2] == 'F':
                    rightPWM = (rightJoyValue)
                    pi.write(IN3R, 0)
                    pi.write(IN4R, 1)
                elif gamepadValues[2] == 'B':
                    rightPWM = (rightJoyValue)
                    pi.write(IN3R, 1)
                    pi.write(IN4R, 0)



        #gamepad control for x and y buttons

        if gamepadValues[4] == 'X': #X button
            #print(gamepadValues[4])
            parent_conn2.send(310)

        if gamepadValues[4] == 'Y': #Y button
            #print(gamepadValues[4])
            parent_conn2.send(311)

        #adjust for minimum pwm for motor to move
        Ladj = 0

        Radj = 0 
            
        pi.set_PWM_dutycycle(PWML, int(leftPWM))        
        pi.set_PWM_dutycycle(PWMR, int(rightPWM))
        
#        print(str(leftPWM) + ' ' + str(rightPWM))        

        #time.sleep(0.1) #100mS


# Using the special variable
# __name__
if __name__=="__main__":
    pi = pigpio.pi()   # init pigpio

    parent_conn,child_conn = Pipe()
    parent_conn2,child_conn2 = Pipe()
    gamepad = Process(target=phone.read, args=(child_conn,))
    gamepad.start()
    sound = Process(target=sound.sound, args=(child_conn2,))
    sound.start()

    main()