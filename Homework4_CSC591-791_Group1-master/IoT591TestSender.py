import time
import ibmiotf.application

client = None

openData = {"timestamp": "timeString goes here", "decision": "The door was opened"}
closeData = {"timestamp": "timeString goes here", "decision": "The door was closed"}

try:
    options = {
        "org": "2nxspc",
        "id": "testsender",
        "type": "standalone",
        "auth-method": "apikey",
        "auth-key": "a-2nxspc-czo3hnx736",
        "auth-token": "GUyIn@Ed8hZewN&&t9"
    }
    client = ibmiotf.application.Client(options)
    client.connect()
    while True:
        client.publishEvent(options["type"], options["id"], "doorOpen", "json", openData)
        print("Sent open door info")
        time.sleep(0.2)
        client.publishEvent(options["type"], options["id"], "doorClose", "json", closeData)
        print("Sent close door info")
        time.sleep(0.2)


except ibmiotf.ConnectionException as e:
    assert isinstance(e, object)
    print(e)