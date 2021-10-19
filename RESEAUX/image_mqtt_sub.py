import paho.mqtt.client as mqtt

MQTT_PATH = "pi19/image/#"
MQTT_SERVER = "192.168.0.214"
MQTT_PORT = 1883

def on_connect(client, userdata, flags, rc):
    print("Connexion established with result code " + str(rc))
    client.subscribe(MQTT_PATH)


def on_message(client, userdata, msg):
    print("ouech")
    nom_image = msg.topic.replace("pi19/image/","").replace("/","")
    print(nom_image)
    f = open('img/'+nom_image, 'wb')
    f.close()
    
    



def main() :

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_SERVER, MQTT_PORT, 60)

    client.loop_forever( )


if __name__ == "__main__":
    main()