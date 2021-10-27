import paho.mqtt.publish as publish
import json
jsonFrame = { }
jsonFrame['dest'] = 'all'
jsonFrame['order'] = 'down'


publish.single('014/shutter/command', json.dumps(jsonFrame), qos=1, hostname='192.168.0.214')
