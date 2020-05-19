import paho.mqtt.client as paho

def on_message(client,userdata,msg):
    print(str(msg.payload.decode('utf-8')))

client = paho.Client()
client.on_message = on_message
client.connect('mqtt.eclipse.org', 1883)
client.subscribe("kmk_geo_api/positions")
print("Started")
client.loop_forever()
