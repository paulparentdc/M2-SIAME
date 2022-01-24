from smbus2 import SMBus
import Adafruit_MCP9808.MCP9808 as MCP9808
import time

bus = SMBus(1)

#Address of I2C devices
devices = []

#Sorted address of I2C devices
temps  = []
lights = []
others = []

#Sensors created using Adafruit library
sensorsT = []

#SRF08 REQUIRES 5V
def scan(force=False):
    devices = []
    for addr in range(0x03, 0x77 + 1):
        read = SMBus.read_byte, (addr,), {'force':force}
        write = SMBus.write_byte, (addr, 0), {'force':force}

        for func, args, kwargs in (read, write):
            try:
                with SMBus(1) as bus:
                    data = func(bus, *args, **kwargs)
                    devices.append(addr)
                    break
            except OSError as expt:
                if expt.errno == 16:
                    # just busy, maybe permanent by a kernel driver or just temporary by some user code
                    pass
    return devices


def taxonomy(devices):
    global lights,temps,others
    for d in devices:
        if d == 57:
            lights.append(d)
        elif d>=24 and d<=31:
            temps.append(d)
        else:
            others.append(d)


def readLight(address):
    bus.write_byte_data(address, 0x08, 0x03)
    time.sleep(0.05)
    val = bus.read_word_data(address, 0xAC)    
    return val


#Main

devices = scan(force=True)
taxonomy(devices)

for d in temps:
    sensor = MCP9808.MCP9808(address=d, busnum=1)
    sensorsT.append({d, sensor})
    sensor.begin()

print("Lights :")
print(lights)
print("Temps :")
print(temps)

while True:
    #write(0x51)
    time.sleep(2)
    print("Temperatures : ")
    for ad, t in sensorsT:
        print( str(ad) + " : " + str(t.readTempC()) )
    
    print("Luminosities : ")
    for l in lights:
        print( str(l) + " : " + str(readLight(l)) )

 
