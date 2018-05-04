import paho.mqtt.client as mqtt
import random
import time
import sys

def on_connect(client, userdata, flags, rc):
        print("From Broker: "+mqtt.connack_string(rc))
        client.publish(topic="status/raspberrypiC", payload="online", qos=2, retain=True)

def on_disconnect(client, userdata, rc):
        client.loop_stop()

def on_publish(client, userdata, mid):
        print("Published Confirmation Message: "+str(mid))

def on_subscribe(client, userdata, mid, granted_qos):
        print ("Subscribe Confirmation Message: "+str(mid))

def on_unsubscribe(client, userdata, mid):
        print ("Unsubscribe Confirmation Message: "+str(mid))

def on_message(client, userdata, message):
        global LAST_PUBLISHED_LIGHTSENSOR
        global LAST_PUBLISHED_THRESHOLD
        global LAST_PUBLISHED_LIGHTSTATUS

        if (message.topic=="lightSensor"):
                LAST_PUBLISHED_LIGHTSENSOR=int(message.payload)
                print (LAST_PUBLISHED_LIGHTSENSOR)
        elif (message.topic=="threshold"):
                LAST_PUBLISHED_THRESHOLD=int(message.payload)
        elif (message.topic=="lightStatus"):
                LAST_PUBLISHED_LIGHTSTATUS=str(message.payload)

HOST=sys.argv[1]
PORTNUMBER=1883
KEEPALIVE=60
BINDADDRESS=""

LAST_PUBLISHED_LIGHTSENSOR=-1
LAST_PUBLISHED_THRESHOLD=-1
LAST_PUBLISHED_LIGHTSTATUS=-1
newLightStatus=""


client = mqtt.Client(client_id="raspberrypiC", clean_session=False, userdata=None, protocol=mqtt.MQTTv311)
client.will_set(topic="status/raspberrypiC", payload="offline", qos=2, retain=True)


client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscribe
client.on_message = on_message

client.connect(HOST, PORTNUMBER, KEEPALIVE, BINDADDRESS)
client.loop_start()

client.subscribe(topic="lightSensor", qos=2)
client.subscribe(topic="threshold", qos=2)
client.subscribe(topic="lightStatus" ,qos=2)

time.sleep(1)

try:
        while True:
                if(LAST_PUBLISHED_LIGHTSENSOR!=-1 and LAST_PUBLISHED_THRESHOLD!=-1):
                        if (int(LAST_PUBLISHED_LIGHTSENSOR)>int(LAST_PUBLISHED_THRESHOLD)):
                                newLightStatus="turnOff"
                        else:
                                newLightStatus="turnOn"

                        if (LAST_PUBLISHED_LIGHTSTATUS!=-1):
                                if (newLightStatus!=LAST_PUBLISHED_LIGHTSTATUS):
                                        client.publish(topic="lightStatus", payload=newLightStatus, qos=2, retain=True)
                        else: client.publish(topic="lightStatus", payload=newLightStatus, qos=2, retain=True)
                time.sleep(1)

except KeyboardInterrupt:
        pass
