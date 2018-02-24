import speech_api as audioStream
import firebase_need_help as fb_help
import os
import time
import servo_control
import RPi.GPIO as GPIO
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

def remote_control_TV(code,channel = '0'):
    TV_direction_x = 0
    TV_direction_y = 90
    servo_control.setServo(TV_direction_x,TV_direction_y)
    if(code=="POWER"):
        os.system('irsend SEND_ONCE /home/pi/lircd.conf KEY_POWER')
    elif(code == "CHANNEL"):
        for num in channel:
            os.system('irsend SEND_ONCE /home/pi/lircd.conf KEY_'+num)
            time.sleep(1)
            
def remote_control_air(code,temp = '0'):
    Air_direction_x = 95
    Air_direction_y = 100
    servo_control.setServo(Air_direction_x,Air_direction_y)
    if(code=="OFF"):
        print(temp)
        os.system('irsend SEND_ONCE air_remote off')
    elif(code == "ON"):
        print(temp)
        os.system('irsend SEND_ONCE air_remote on_'+temp+'C')

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
    print("helping support system is working...")
    fb_help.putData('1101','YES')
    print("Your request has been sent")
def start(air_temp):
    print("System starting")
    air_trig = 0
    light_trig = 0
    tv_trig = 0
    command = audioStream.main()
    print("Translating command")
    print(command)
    for word in turn_on_light:
        if word in command and light_trig == 0:
            print("Turning on light...")
            lightCode = 1
            size = len(word)
            index = command.find(word)
            cut_word = command[index+size:-1]
            if "ห้องนอน" in cut_word and "ห้องน้ำ" in cut_word:
                lightCode = 1
            elif "ห้องนอน" in cut_word :
                lightCode = 2
            elif "ห้องน้ำ" in cut_word :
                lightCode = 3
                
            lightControl(GPIO.HIGH,lightCode)
            light_trig = 1
            print("Done")
            break;
    
    for word in turn_off_light:
        if (word in command) and light_trig == 0:
            print("Turning off light...")
            lightCode = 1
            size = len(word)
            index = command.find(word)
            cut_word = command[index+size:-1]
            if "1" in cut_word and "2" in cut_word:
                lightCode = 1
            elif "1" in cut_word :
                lightCode = 2
            elif "2" in cut_word :
                lightCode = 3
                
            lightControl(GPIO.LOW,lightCode)
            light_trig = 1
            print("Done")
            break;
    for word in turn_on_tv:
        if(word in command ):
            print("Turning on TV")
            tv_trig = 1
            remote_control_TV("POWER")
            print("Done")
            break

    for word in turn_off_tv:
        if(word in command and tv_trig == 0):
            print("Turning off TV")
            remote_control_TV("POWER")
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
    for word in need_help:
        if word in command:
            helpingSupport()
            break;

    for word in turn_on_air:
        if word in command and air_trig == 0:
            print("Turning on air conditioner")
            remote_control_air("ON",str(air_temp))
            air_trig = 1
            break;
        
    for word in turn_off_air:
        if word in command and air_trig == 0:
            print("Turning off air conditioner")
            remote_control_air("OFF")
            air_trig = 1
            break;

    for word in increase_air_temp:
        if(word in command):
            print("Increasing air temperature from ",air_temp," to ",air_temp+1)
            air_temp += 1
            air_temp_str = str(air_temp)
            remote_control_air("ON",air_temp_str)
            break;

    for word in decrease_air_temp:
        if(word in command):
            print("Decreasing air temperature  from ",air_temp," to ",air_temp-1)
            air_temp -= 1
            air_temp_str = str(air_temp)
            remote_control_air("ON",air_temp_str)
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
    return air_temp
def waitForStart(air_temp):
    
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
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(light1,GPIO.OUT)
GPIO.setup(light2,GPIO.OUT)
GPIO.setup(button,GPIO.IN)
GPIO.setup(servo1_pin,GPIO.OUT)
GPIO.setup(servo2_pin,GPIO.OUT)
while True:
    air_temp = waitForStart(air_temp)
#for word in change_temp_air_first:
#    if (word in command) and (change_temp_air_last in command):
#        temp_str = list(filter(str.isdigit, command))
#        temp_value = int(''.join(temp_str))
#        remote_control(2,int(temp_value))
#        break;