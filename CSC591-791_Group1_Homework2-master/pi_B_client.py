import paho.mqtt.client as mqtt
import random
import time
import sys
import RPi.GPIO as GPIO


#arguments:
#               1) Broker IP
#               2) LED 1 input pin number
#               3) LED 2 input pin number
#               4) LED 3 input pin number


def setup_pins(pin1, pin2, pin3):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(pin1,GPIO.OUT)
        GPIO.setup(pin2,GPIO.OUT)
        GPIO.setup(pin3,GPIO.OUT)

def on_connect(client, userdata, flags, rc):
        print("From Broker: "+mqtt.connack_string(rc))
        client.publish(topic="status/raspberrypiB", payload="online", qos=2, retain=True)

def on_disconnect(client, userdata, rc):
        client.publish(topic="status/raspberrypiB", payload="offline", qos=2, retain=True)
        client.loop_stop()
        GPIO.cleanup()

def on_publish(client, userdata, mid):
        print("Publish Confirmation Message: "+str(mid))

def on_subscribe(client, userdata, mid, granted_qos):
        print ("Subscribe Confirmation Message: "+str(mid))

def on_unsubscribe(client, userdata, mid):
        print ("Unsubscribe Confirmation Message: "+str(mid))

def on_message(client, userdata, message):
        global PI_A_STATUS
        global PI_C_STATUS
        global LIGHT_STATUS
        if (message.topic=="status/raspberrypiA"):
                if(message.payload=="online"):
                        PI_A_STATUS=True
                elif(message.payload=="offline"):
                        PI_A_STATUS=False

        if (message.topic=="status/raspberrypiC"):
                if(message.payload=="online"):
                        PI_C_STATUS=True
                elif(message.payload=="offline"):
                        PI_C_STATUS=False


        if (message.topic=="lightStatus"):
                if (message.payload=="turnOn"):
                        LIGHT_STATUS=True
                elif(message.payload=="turnOff"):
                        LIGHT_STATUS=False

def ledStatus(status, pin):
        if (status==True):
                GPIO.output(pin, GPIO.HIGH)
        else: GPIO.output(pin, GPIO.LOW)


HOST=sys.argv[1]
PORTNUMBER=1883
KEEPALIVE=60
BINDADDRESS=""

LED_1_PIN=int(sys.argv[2])
LED_2_PIN=int(sys.argv[3])
LED_3_PIN=int(sys.argv[4])


PI_A_STATUS=None
PI_C_STATUS=None
LIGHT_STATUS=None

setup_pins(LED_1_PIN, LED_2_PIN, LED_3_PIN)

client = mqtt.Client(client_id="raspberrypiB", clean_session=False, userdata=None, protocol=mqtt.MQTTv311)
client.will_set(topic="status/raspberrypiB", payload="offline", qos=2, retain=True)


client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscribe
client.on_message = on_message


client.connect(HOST, PORTNUMBER, KEEPALIVE, BINDADDRESS)
client.loop_start()

client.subscribe(topic="lightStatus", qos=2)
client.subscribe(topic="status/raspberrypiA", qos=2)
client.subscribe(topic="status/raspberrypiC", qos=2)

time.sleep(1)

try:
        while True:
                if (LIGHT_STATUS!=None):
                        if (LIGHT_STATUS==True):
                                ledStatus(True, LED_1_PIN)
                        else: ledStatus(False, LED_1_PIN)

                if (PI_A_STATUS!=None):
                        if (PI_A_STATUS==True):
                                ledStatus(True, LED_2_PIN)
                        else: ledStatus(False, LED_2_PIN)

                if (PI_C_STATUS!=None):
                        if (PI_C_STATUS==True):
                                ledStatus(True, LED_3_PIN)
                        else: ledStatus(False, LED_3_PIN)

                time.sleep(0.5)

except KeyboardInterrupt:
        GPIO.cleanup()
