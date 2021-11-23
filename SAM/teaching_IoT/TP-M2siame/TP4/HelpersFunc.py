
import smbus2

def i2cscan(busnum =-1):
    _IC2_ADDR_RANGE = 128

    try:
        bus = smubus.SMBus(busnum if busnum >= 0 else 1)
    except IOError as err:
        print("[%s] i2c busnum '%d' does not seem toexist!" % (__name__,busnum))
        return
    devicesList = []
    



