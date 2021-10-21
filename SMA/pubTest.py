import paho.mqtt.publish as publish
import json
jsonFrame = { }
jsonFrame['order'] = 'capture'
jsonFrame['value'] = '15:12:35'


publish.single('pi19/image/command', json.dumps(jsonFrame), qos=1, hostname='192.168.0.214')
