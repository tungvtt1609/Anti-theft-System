import telepot
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
from time import sleep
import datetime
from telepot.loop import MessageLoop
from subprocess import call 
 
 
PIR = 4 #khai báo chân cảm biến
GPIO_ECHO = 24
GPIO_TRIGGER = 18
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 25
 
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR, GPIO.IN)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.OUT)
 
motion = 0
motionNew = 0

 
def handle(msg):
    global telegramText
    global chat_id
    
    chat_id = msg['chat']['id']
    telegramText = msg['text']
    
    print('Message received from ' + str(chat_id))
    
    if telegramText == '/start':
        bot.sendMessage(chat_id, 'Security camera is activated.')#Put your welcome note here
    
    while True:
        main()

bot = telepot.Bot("5452453117:AAGgOPQ5cK30rSSOFUo05E72Os08pLh6hok")
bot.message_loop(handle)

def main():
    global chat_id
    global motion
    global motionNew

    if GPIO.input(GPIO_ECHO) == 1:
        print("Motion detected")
        motion = 1
        if motionNew != motion:
            motionNew = motion
            sendNotification(motion)
    elif GPIO.input(GPIO_ECHO) == 0:
        print("No motion detected")
        motion = 0
        if motionNew != motion:
            motionNew = motion

def sendNotification(motion): 
 
    global chat_id

    if motion == 1:
        filename = "./video_" + (time.strftime("%y%b%d_%H%M%S"))
        camera.start_recording(filename + ".h264")
        sleep(5)
        camera.stop_recording()
        command = "MP4Box -add " + filename + '.h264' + " " + filename + '.mp4'
        print(command)
        call([command], shell=True)
        bot.sendVideo(chat_id, video = open(filename + '.mp4', 'rb'))
        bot.sendMessage(chat_id, 'The motion sensor is triggered!')

while True:
    time.sleep(10)

 
 
 
