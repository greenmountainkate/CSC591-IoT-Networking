import paho.mqtt.client as mqtt
import random
import time
import sys
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

#aruments:
#               1) broker IP
#               2) LDR threshold
#               3) Potentiometer threshold
#               4) LDR channel
#               5) Potentiometer channel

mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(0, 0))

def on_connect(client, userdata, flags, rc):
        print("From Broker: "+mqtt.connack_string(rc))
        client.publish(topic="status/raspberrypiA", payload="online", qos=2, retain=True)

def on_disconnect(client, userdata, rc=0):
        client.publish(topic="status/raspberrypiA", payload="offline", qos=2, retain=True)
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

        if (message.topic=="lightSensor"):
                LAST_PUBLISHED_LIGHTSENSOR=int(message.payload)
        elif (message.topic=="threshold"):
                LAST_PUBLISHED_THRESHOLD=int(message.payload)

HOST=sys.argv[1]
PORTNUMBER=1883
KEEPALIVE=60
BINDADDRESS=""

LDR_THRESH=int(sys.argv[2])
POT_THRESH=int(sys.argv[3])
LDR_CHANNEL=int(sys.argv[4])
POT_CHANNEL=int(sys.argv[5])


SAMPLE_INTERVAL=1
LAST_PUBLISHED_LIGHTSENSOR=-1
LAST_PUBLISHED_THRESHOLD=-1

client = mqtt.Client(client_id="raspberrypiA", clean_session=False, userdata=None, protocol=mqtt.MQTTv311)
client.will_set(topic="status/raspberrypiA", payload="offline", qos=2, retain=True)


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

time.sleep(1)

try:

        if (LAST_PUBLISHED_LIGHTSENSOR==-1):
                lightSensor= int(mcp.read_adc(LDR_CHANNEL))
                client.publish(topic="lightSensor", payload=lightSensor, qos=2, retain=True)

        if (LAST_PUBLISHED_THRESHOLD==-1):
                threshold= int(mcp.read_adc(POT_CHANNEL))
                client.publish(topic="threshold", payload=threshold, qos=2, retain=True)

        while True:

                lightSensor= int(mcp.read_adc(LDR_CHANNEL))
                if (((LAST_PUBLISHED_LIGHTSENSOR+LDR_THRESH)<lightSensor) or ((LAST_PUBLISHED_LIGHTSENSOR-LDR_THRESH)>lightSensor)):
                        client.publish(topic="lightSensor", payload=lightSensor, qos=2, retain=True)


                threshold= int(mcp.read_adc(POT_CHANNEL))
                if (((LAST_PUBLISHED_THRESHOLD+POT_THRESH)<threshold) or ((LAST_PUBLISHED_THRESHOLD-POT_THRESH)>threshold)):
                        client.publish(topic="threshold", payload=threshold, qos=2, retain=True)

                print ("Sensor: "+str(lightSensor) +"\t\t\t" + "Threshold: "+str(threshold))
                print ('-' * 70)

                time.sleep(SAMPLE_INTERVAL)

except KeyboardInterrupt:
        pass
