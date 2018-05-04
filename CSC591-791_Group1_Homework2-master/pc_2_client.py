import paho.mqtt.client as mqtt
import random
import time
import datetime
import sys
import io


def on_disconnect(client, userdata, rc):
	client.loop_stop()

def on_message(client, userdata, message):
	print("| %40s | %40s | %40s |"%(message.topic.center(40,' '), message.payload.center(40,' '), datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S').center(40,' ')))
	if (message.topic=="lightStatus"):
		f=open("lightStatus.txt", "a+")
		f.write("| %40s | %40s | %40s |"%(message.topic.center(40,' '), message.payload.center(40,' '), datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S').center(40,' ')))
		f.close()
		


HOST=sys.argv[1]
PORTNUMBER=1883
KEEPALIVE=60
BINDADDRESS=""


client = mqtt.Client(client_id="pc2", clean_session=True, userdata=None, protocol=mqtt.MQTTv311)


client.on_disconnect = on_disconnect
client.on_message = on_message


client.connect(HOST, PORTNUMBER, KEEPALIVE, BINDADDRESS)
client.loop_start()

client.subscribe(topic="lightSensor", qos=2)
client.subscribe(topic="threshold", qos=2)
client.subscribe(topic="lightStatus", qos=2)
client.subscribe(topic="status/raspberrypiA", qos=2)
client.subscribe(topic="status/raspberrypiB", qos=2)
client.subscribe(topic="status/raspberrypiC", qos=2)

print("Subscribed to the topics: lightSensor, threshold, lightStatus, status/raspberrypiA, status/raspberrypiB, status/raspberrypiC")
print("| %40s | %40s | %40s |"%("Topic".center(40,' '), "Payload".center(40,' '), "Time Stamp".center(40,' ')))
print('-' * 130)
try:
	while True:
		time.sleep(0.5)
except KeyboardInterrupt:
	client.disconnect()
