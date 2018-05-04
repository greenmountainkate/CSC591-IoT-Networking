import time
import ibmiotf.application


client = None

def mcc(door_event):

    if door_event.event == "doorOpen":
        #print("Got Door Open Event")
        print("{} - {}".format(door_event.data["timestamp"], door_event.data["decision"] ))

    elif door_event.event == "doorClose":
        #print("Got Door Close Event")
        print("{} - {}".format(door_event.data["timestamp"], door_event.data["decision"]))


try:

    options = {
        "org": "2nxspc",
        "id": "receiver",
        "type": "standalone",
        "auth-method": "apikey",
        "auth-key": "a-2nxspc-czo3hnx736",
        "auth-token": "GUyIn@Ed8hZewN&&t9"
    }
    client = ibmiotf.application.Client(options)
    client.connect()
    client.deviceEventCallback = mcc
    client.subscribeToDeviceEvents(event="doorOpen")
    client.subscribeToDeviceEvents(event="doorClose")

    while True:
        time.sleep(0.2)

except ibmiotf.ConnectionException as e:
    assert isinstance(e, object)
    print(e)
