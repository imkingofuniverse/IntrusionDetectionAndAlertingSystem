import RPi.GPIO as GPIO
import time
from subprocess import call
import pygame
import smtplib,ssl
from picamera import PiCamera  
from time import sleep  
from email.mime.multipart import MIMEMultipart  
from email.mime.base import MIMEBase  
from email.mime.text import MIMEText  
from email.utils import formatdate  
from email import encoders


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
        def send_an_email():  
            toaddr = 'intruderalertingsystem@gmail.com'      # To id 
            me = 'intruderalertingsystem@gmail.com'          # your id
            subject = "Fire Alert"              # Subject
          
            msg = MIMEMultipart()  
            msg['Subject'] = subject  
            msg['From'] = me  
            msg['To'] = toaddr  
            msg.preamble = "test "   
            #msg.attach(MIMEText(text))  
      
            part = MIMEBase('application', "octet-stream")  
            part.set_payload(open("fire.jpeg", "rb").read())  
            encoders.encode_base64(part)  
            part.add_header('Content-Disposition', 'attachment; filename="fire.jpeg"')   # File name and format name
            msg.attach(part)  
          
            try:  
               s = smtplib.SMTP('smtp.gmail.com', 587)  # Protocol
               s.ehlo()  
               s.starttls()  
               s.ehlo()  
               s.login(user = 'intruderalertingsystem@gmail.com', password = 'jarvis@123')  # User id & password
               #s.send_message(msg)  
               s.sendmail(me, toaddr, msg.as_string())  
               s.quit()  
            #except:  
            #   print ("Error: unable to send email")    
            except SMTPException as error:  
                  print ("Error")                # Exception
          
        send_an_email()  

    
    if distance<50:
        call(["espeak","-s140 -ven+18 -z","Intruder Alert"])
        pygame.mixer.init()
        pygame.mixer.music.load("siren.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        def send_an_email():  
            toaddr = 'intruderalertingsystem@gmail.com'      # To id 
            me = 'intruderalertingsystem@gmail.com'          # your id
            subject = "Intruder Alert"              # Subject
          
            msg = MIMEMultipart()  
            msg['Subject'] = subject  
            msg['From'] = me  
            msg['To'] = toaddr  
            msg.preamble = "test "   
            #msg.attach(MIMEText(text))  
      
            part = MIMEBase('application', "octet-stream")  
            part.set_payload(open("intruder.png", "rb").read())  
            encoders.encode_base64(part)  
            part.add_header('Content-Disposition', 'attachment; filename="intruder.png"')   # File name and format name
            msg.attach(part)  
          
            try:  
               s = smtplib.SMTP('smtp.gmail.com', 587)  # Protocol
               s.ehlo()  
               s.starttls()  
               s.ehlo()  
               s.login(user = 'intruderalertingsystem@gmail.com', password = 'jarvis@123')  # User id & password
               #s.send_message(msg)  
               s.sendmail(me, toaddr, msg.as_string())  
               s.quit()  
            #except:  
            #   print ("Error: unable to send email")    
            except SMTPException as error:  
                  print ("Error")                # Exception
          
        send_an_email()  

