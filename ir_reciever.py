import lirc
import time
soclid = lirc.init("myprogram",blocking=False)
while True:
    try:
        button = lirc.nextcode()
        #print("Press RC button")
        if len(button) == 0: continue
        print(button[0])
        time.sleep(1)
    except KeyboardInterrupt:
        lirc.deinit()
        break