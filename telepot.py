import telepot                  #setup thư viện sử dụng telegram bot
from telepot.loop import MessageLoop #setup thư viện sử dụng telegram bot
from picamera import PiCamera   #setup thư viện để sử dụng camera
import RPi.GPIO as GPIO   #setup thư viện để sử dụng GPIO của máy tính nhúng
import time    #setup thư viện thời gian
from time import sleep   #setup thư viện thời gian
import datetime   #setup thư viện thời gian
from subprocess import call 
 
 
PIR = 4 #khai báo chân cảm biến
camera = PiCamera()  #khai báo camera
camera.resolution = (640, 480)  #khai báo độ phân giải cho camera
camera.framerate = 25  #khai báo chân camera
 
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)  #set mode hoạt động BCM/BOARD
GPIO.setup(PIR, GPIO.IN)  #set chân cảm biến là đầu vào
 
motion = 0   #khai báo trạng thái chuyển động của cảm biến
motionNew = 0   #khai báo trạng thái chuyển động mới nhất của cảm biến

 
def handle(msg):   #hàm kích hoạt trạng thái hoạt động cho hệ thống
    global telegramText  #khai báo biến
    global chat_id   #khai báo biến
    
    chat_id = msg['chat']['id']   #định dạng biến chat_id
    telegramText = msg['text']    #định dạng biến telegramText
    
    print('Message received from ' + str(chat_id))    #in trạng thái
    
    if telegramText == '/start':   #kiểm tra điều kiện kích hoạt
        bot.sendMessage(chat_id, 'Security camera is activated.')   #chat_bot gửi tín hiệu hoạt động
    
    while True:   #vòng lặp cho hàm main
        main()

bot = telepot.Bot("5452453117:AAGgOPQ5cK30rSSOFUo05E72Os08pLh6hok")   #cú pháp thực hiện chèn api token telegram của chat_bot
bot.message_loop(handle)   #thực hiện gửi bản tin

def main():   #hàm main chính của chương trình
    global chat_id
    global motion
    global motionNew

    if GPIO.input(PIR) == 1:   #kiểm tra điều kiện đầu vào của cảm biến 
        print("Motion detected")   #in ra trạng thái có chuyển động
        motion = 1
        if motionNew != motion:    #kiểm tra điều kiện so sánh giữa 2 biến trạng thái
            motionNew = motion     
            sendNotification(motion)  #hàm gửi tín hiệu thông báo
    elif GPIO.input(PIR) == 0:  #kiểm tra điều kiện đầu vào của cảm biến
        print("No motion detected")   #in ra trạng thái không chuyển động
        motion = 0
        if motionNew != motion:     #kiểm tra điều kiện so sánh giữa 2 biến trạng thái
            motionNew = motion

def sendNotification(motion):   #hàm thực hiện gửi tín hiệu thông báo
 
    global chat_id

    if motion == 1:  #kiểm tra điều kiện có chuyển động
        filename = "./video_" + (time.strftime("%y%b%d_%H%M%S"))  
        camera.start_recording(filename + ".h264")    #bắt đầu record video
        sleep(5)
        camera.stop_recording()   #dừng record video
        command = "MP4Box -add " + filename + '.h264' + " " + filename + '.mp4'   #định dạng video
        print(command)
        call([command], shell=True)
        bot.sendVideo(chat_id, video = open(filename + '.mp4', 'rb'))  #gửi video đến chat_bot
        bot.sendMessage(chat_id, 'The motion sensor is triggered!')    #gửi trạng thái đến chat_bot

while True:
    time.sleep(10)

 
 
 
