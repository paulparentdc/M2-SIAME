import paho.mqtt.client as mqtt
import logging as log


MQTT_PATHS = {"pi19/image/light/#","pi19/image/dark/#"}
MQTT_SERVER = "192.168.0.214"
MQTT_PORT = 1883

def on_connect(client, userdata, flags, rc):
    print("Connexion established with result code " + str(rc))
    client.subscribe("pi19/image/light/#")
    client.subscribe("pi19/image/dark/#")

    for path in MQTT_PATHS:
        # subscribe to topics list

            print("    subscribing to " + path)
            client.subscribe(path)




def on_message(client, userdata, msg):
    print("Message received : ")
    if(msg.topic.startswith("pi19/image/light/")):
        # getting the image's name
        nom_image = msg.topic.replace("pi19/image/light/","").replace("/","")
        f = open('img/light/'+nom_image, 'wb')
        print("   Image received : light")
        try:
            # loading payload and writing image
            f.write(msg.payload)
        except Exception as ex:
            log.error("exception loading image payload '%s': " % str(msg.topic) + str(ex))
            return
        f.close()


    elif(msg.topic.startswith("pi19/image/dark/")):
        # getting the image's name
        nom_image = msg.topic.replace("pi19/image/dark/","").replace("/","")
        f = open('img/dark/'+nom_image, 'wb')
        print("   Image received : dark")
        try:
            # loading payload and writing image
            f.write(msg.payload)
        except Exception as ex:
            log.error("exception loading image payload '%s': " % str(msg.topic) + str(ex))
            return
        f.close()
    else:
        print("Message received but in the wrong topic")   
    



def main() :

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_SERVER, MQTT_PORT, 60)

    client.loop_forever( )


if __name__ == "__main__":
    main()