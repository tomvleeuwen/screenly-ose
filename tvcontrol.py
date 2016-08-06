import time
import sys
from settings import settings

sys.path.append("/home/pi/screenly/python-cec")
import cec

sleep = 30

def tv_keep_on(tvdev):
    settings.load()
    power_on = settings["tv_power_on"]
    active_source = settings["tv_active_source"]
    
    print "Power on: %s, active_source: %s" % (power_on, active_source)
    
    if power_on:
        tvdev.power_on()
    time.sleep(sleep)
    
    if active_source:
        cec.set_active_source()
    time.sleep(sleep)
    
def main():
    adapters = cec.list_adapters()
    cec.init(adapters[0])
    devices = cec.list_devices()
    # weird it is a dictionary, mine (no TV connected) is not empty but only contains "1" but not "0". 
    # Tom wants 0 so wait for it
    while ( "0" not in devices ):
       print("Devices: "+str(devices))
       print("Correct CEC device not detected. Waiting....")
       time.sleep(10)
       devices = cec.list_devices()

    tvdev = devices[0]
    
    while True:
        tv_keep_on(tvdev)

if __name__ == "__main__":
    main()    
