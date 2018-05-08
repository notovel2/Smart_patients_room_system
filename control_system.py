import speech_api as audioStream
import firebase_need_help as fb
import line_notify
import os
import time
import servo_control
import RPi.GPIO as GPIO
import sys
turn_on_light = ["เปิดไฟ"]
turn_off_light = ["ปิดไฟ"]

need_help = ["ช่วยด้วย","เรียกพยาบาล"]

turn_on_air = ["เปิดแอร์","เปิดเครื่องปรับอากาศ"]
turn_off_air = ["ปิดแอร์","ปิดเครื่องปรับอากาศ"]
increase_air_temp = ["เพิ่มแอร์","เพิ่มAir","เพิ่ม Air"]
decrease_air_temp = ["เบาแอร์","ลดแอร์","รถแอร์"]
change_temp_air = ["ปรับแอร์"]
#change_temp_air_last = "องศา"

turn_on_tv = ["เปิดทีวี","เปิดโทรทัศน์"]
turn_off_tv = ["ปิดทีวี","ปิดโทรทัศน์"]
change_channel_tv = ["เปลี่ยนเป็นช่อง"]
air_temp = 25
#TV_direction_x = 20
#TV_direction_y = 100
#Air_direction_x = 90
#Air_direction_y = 120
button = 40
servo1_pin = 23
servo2_pin = 24
light1 = 37
light2 = 38

led_g = 33
led_y = 36
led_r = 35

room = '1101'

def set_led(R,G,Y):
    r = GPIO.LOW
    g = GPIO.LOW
    y = GPIO.LOW
    if R == 1 :
        r = GPIO.HIGH
    if Y == 1:
        y = GPIO.HIGH
    if G == 1 :
        g = GPIO.HIGH
    GPIO.output(led_r,r)
    GPIO.output(led_y,y)
    GPIO.output(led_g,g)

def remote_control_TV(code,channel = '0'):
    TV_direction_x = 75
    TV_direction_y = 100
    servo_control.setServo(TV_direction_x,TV_direction_y)
    if(code=="POWER"):
        os.system('irsend SEND_ONCE TV_1 KEY_POWER')
    elif(code == "CHANNEL"):
        for num in channel:
            os.system('irsend SEND_ONCE TV_1 KEY_'+num)
            time.sleep(1)
            
def remote_control_air(code,temp = '0'):
    Air_direction_x = 0
    Air_direction_y = 130
    servo_control.setServo(Air_direction_x,Air_direction_y)
    if(code=="OFF"):
        print(temp)
        os.system('irsend SEND_ONCE air_remote_1 off')
    elif(code == "ON"):
        print(temp)
        os.system('irsend SEND_ONCE air_remote_1 on_'+temp+'C')

def remote_control(code,temp = 0):
    print("remote control system is working...")
def lightControl(code,lightCode):
    
    print("light control system is working...")
    
    if lightCode == 1 or lightCode == 2:
        print("light 1 working")
        GPIO.output(light1,code)
    if lightCode == 1 or lightCode == 3:
        print("light 2 working")
        GPIO.output(light2,code)
def helpingSupport():
    print("sending a notification")
    #fb_help.putData('1101','YES')
    line_notify.line_notify_text("Room "+room+" need help!!")
    print("Your request has been sent")
def start(air_temp):
    set_led(1,0,0)
    print("System starting")
    air_trig = 0
    light_trig = 0
    tv_trig = 0
    command = audioStream.main(client)
    set_led(1,0,0)
    print("Translating command")
    print(command)
    for word in turn_on_light:
        if word in command and light_trig == 0:
            print("Turning on light...")
            lightCode = 1
            size = len(word)
            index = command.find(word)
            cut_word = command[index+size:-1]
            print("Word: ",cut_word)
            temp_command = "turn on light"
            if "ห้องนอน" in cut_word and "ห้องน้ำ" in cut_word:
                lightCode = 1
            elif "ห้องนอน" in cut_word :
                lightCode = 2
                temp_command = temp_command+" bedroom"
            elif "ห้องน้ำ" in cut_word :
                lightCode = 3
                temp_command = temp_command+" bathroom"
                
            lightControl(GPIO.HIGH,lightCode)
            light_trig = 1
            fb.postData(temp_command,room)
            print("Done")
            break;
    
    for word in turn_off_light:
        if (word in command) and light_trig == 0:
            print("Turning off light...")
            lightCode = 1
            size = len(word)
            index = command.find(word)
            cut_word = command[index+size:-1]
            temp_command = "turn off light"
            if "ห้องนอน" in cut_word and "ห้องน้ำ" in cut_word:
                lightCode = 1
            elif "ห้องนอน" in cut_word :
                lightCode = 2
                temp_command = temp_command+" bedroom"
            elif "ห้องน้ำ" in cut_word :
                lightCode = 3
                temp_command = temp_command+" bathroom"
                
            lightControl(GPIO.LOW,lightCode)
            light_trig = 1
            fb.postData(temp_command,room)
            print("Done")
            break;
    for word in turn_on_tv:
        if(word in command ):
            print("Turning on TV")
            tv_trig = 1
            remote_control_TV("POWER")
            temp_command = "turn on TV"
            fb.postData(temp_command,room)
            print("Done")
            break

    for word in turn_off_tv:
        if(word in command and tv_trig == 0):
            print("Turning off TV")
            remote_control_TV("POWER")
            temp_command = "turn on TV"
            fb.postData(temp_command,room)
            print("Done")
            break
    for word in change_channel_tv:
        if(word in command):
            
            size = len(word)
            index = command.find(word)
            cut_word = command[index+size:-1]
            temp_value = [s for s in cut_word.split() if s.isdigit()]
            if(not (temp_value[0] is None)):
                print("Changing TV channel ",temp_value[0])
                #print(temp_value[0])        
                remote_control_TV("CHANNEL",temp_value[0])
                temp_command = "changed tv channel to "+temp_value[0]
                fb.postData(temp_command,room)
    for word in need_help:
        if word in command:
            helpingSupport()
            temp_command = "call for help"
            fb.postData(temp_command,room)
            break;

    for word in turn_on_air:
        if word in command and air_trig == 0:
            print("Turning on air conditioner")
            remote_control_air("ON",str(air_temp))
            temp_command = "turn on air"
            fb.postData(temp_command,room)
            air_trig = 1
            break;
        
    for word in turn_off_air:
        if word in command and air_trig == 0:
            print("Turning off air conditioner")
            remote_control_air("OFF")
            temp_command = "turn off air"
            fb.postData(temp_command,room)
            air_trig = 1
            break;

    for word in increase_air_temp:
        if(word in command):
            print("Increasing air temperature from ",air_temp," to ",air_temp+1)
            air_temp += 1
            air_temp_str = str(air_temp)
            remote_control_air("ON",air_temp_str)
            temp_command = "increase air temperature"
            fb.postData(temp_command,room)
            break;

    for word in decrease_air_temp:
        if(word in command):
            print("Decreasing air temperature  from ",air_temp," to ",air_temp-1)
            air_temp -= 1
            air_temp_str = str(air_temp)
            remote_control_air("ON",air_temp_str)
            temp_command = "decrease air temperature"
            fb.postData(temp_command,room)
            break;

    for word in change_temp_air:
        if(word in command):
            
            size = len(word)
            index = command.find(word)
            cut_word = command[index+size:-1]
            temp_value = [s for s in cut_word.split() if s.isdigit()]
            if(not (temp_value[0] is None)):
                print("Changing air temperature to  ",temp_value[0])
                air_temp = int(temp_value[0])
                #print(temp_value[0])        
                remote_control_air("ON",temp_value[0])
                temp_command = "change air temp to "+temp_value[0]+"C"
                fb.postData(temp_command,room)
    return air_temp

    
def waitForStart(air_temp):
    set_led(0,0,1)
    state = GPIO.input(button)
    last_state = state
    print("push a button to start the system")
    while True:
        
        state = GPIO.input(button)
        #print(last_state,state)
        if state == 1 and state != last_state:
            break
        last_state = state
    air_temp = start(air_temp)
    return air_temp
def led_init():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(light1,GPIO.OUT)
    GPIO.setup(light2,GPIO.OUT)
    GPIO.setup(button,GPIO.IN)
    GPIO.setup(servo1_pin,GPIO.OUT)
    GPIO.setup(servo2_pin,GPIO.OUT)
    GPIO.setup(led_r,GPIO.OUT)
    GPIO.setup(led_g,GPIO.OUT)
    GPIO.setup(led_y,GPIO.OUT)
led_init()
print("Connecting to Google Speech API")
client = audioStream.init() 
while True:    
    try:
        
        set_led(1,0,0)
        
        while True:
            air_temp = waitForStart(air_temp)
    except KeyboardInterrupt:        
        set_led(0,0,0)
        GPIO.cleanup()
        sys.exit()
    except:
        print("System has down ,rebooting system")
        temp_command = "ERROR"
        fb.postData(temp_command,room)
        
#for word in change_temp_air_first:
#    if (word in command) and (change_temp_air_last in command):
#        temp_str = list(filter(str.isdigit, command))
#        temp_value = int(''.join(temp_str))
#        remote_control(2,int(temp_value))
#        break;