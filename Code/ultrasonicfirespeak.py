import RPi.GPIO as GPIO
import time
from subprocess import call
import pygame
TRIG=21
ECHO=18
#GPIO SETUP
channel = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
GPIO.setwarnings(False)


while True:
    print("distance measurement in progress")
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG,False)
    print("waiting for sensor to settle")
    time.sleep(0.2)
    GPIO.output(TRIG,True)
    time.sleep(0.00001)
    GPIO.output(TRIG,False)
    while GPIO.input(ECHO)==0:
        pulse_start=time.time()
    while GPIO.input(ECHO)==1:
        pulse_end=time.time()
    pulse_duration=pulse_end-pulse_start
    distance=pulse_duration*17150
    distance=round(distance,2)
    print("distance:",distance,"cm")
    time.sleep(2)
    
    if(GPIO.input(20)==False):
        print("flame detected")
        call(["espeak","-s140 -ven+18 -z","Fire Detected"])

    
    if distance<50:
        call(["espeak","-s140 -ven+18 -z","Intruder Alert"])
        pygame.mixer.init()
        pygame.mixer.music.load("siren.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
