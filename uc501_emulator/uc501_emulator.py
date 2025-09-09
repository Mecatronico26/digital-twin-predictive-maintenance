# uc501_emulator/uc501_emulator.py
import json
import paho.mqtt.client as mqtt

class UC501Emulator:
    def __init__(self, threshold=4.5):
        self.threshold = threshold

    def process(self, payload):
        rms_z = payload['vibration']['z']['rms']
        if rms_z > self.threshold:
            payload['event'] = "ANOMALY_DETECTED"
            payload['alarm_threshold'] = self.threshold
            return payload, True
        else:
            payload['event'] = "HEARTBEAT"
            return payload, False

# Suscribirse a simulador, publicar en "LoRaWAN virtual"
client = mqtt.Client()

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    uc501 = UC501Emulator(threshold=4.5)
    new_payload, is_alarm = uc501.process(payload)
    topic = "lora/uc501/alarm" if is_alarm else "lora/uc501/heartbeat"
    client.publish(topic, json.dumps(new_payload))
    print(f"UC501: {topic} -> {new_payload['sensor_id']}")

client.on_message = on_message
client.connect("localhost", 1883, 60)
client.subscribe("sensors/simulated/data")
client.loop_forever()