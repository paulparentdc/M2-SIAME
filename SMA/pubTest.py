import paho.mqtt.publish as publish
import json
jsonFrame = { }
jsonFrame['dest'] = 'b8:27:eb:cf:2c:f6'
jsonFrame['order'] = 'capture'
jsonFrame['value'] = '15'


publish.single('1R1/014/temperature/command', json.dumps(jsonFrame), qos=1, hostname='192.168.0.214')
