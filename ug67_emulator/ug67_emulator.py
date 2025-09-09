# ug67_emulator/ug67_emulator.py
import json
import paho.mqtt.client as mqtt

client = mqtt.Client()

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    # Publica en el topic final que Node-RED escucha
    client.publish(f"sensors/{payload['sensor_id']}/data", json.dumps(payload))
    print(f"UG67: Reenviado a sensors/{payload['sensor_id']}/data")

client.on_message = on_message
client.connect("localhost", 1883, 60)
client.subscribe("lora/uc501/#")  # Escucha alarmas y heartbeats
client.loop_forever()