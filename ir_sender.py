import os
key = str(input('enter input : '))
print(key)

os.system('irsend SEND_ONCE /home/pi/lircd.conf KEY_'+key)

