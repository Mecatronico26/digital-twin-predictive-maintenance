# simulator/sensor_simulator.py
import time
import json
import random
import paho.mqtt.client as mqtt

class LHSensorSimulator:
    def __init__(self, sensor_id, rpm=1750, mode="normal"):
        self.sensor_id = sensor_id
        self.rpm = rpm
        self.mode = mode
        self.t = 0

    def generate_vibration(self):
        base = 2.5 + 0.5 * random.uniform(-1, 1)
        if self.mode == "bearing_failure":
            base += 0.1 * (self.t / 3600)
            if self.t % 300 < 10:
                base += random.uniform(1.5, 2.5)
        elif self.mode == "pid_oscillation":
            base += 1.5 * random.uniform(-1, 1)
        noise = [random.gauss(0, 0.2) for _ in range(3)]
        return [base + noise[i] for i in range(3)]

    def generate_temperature(self):
        base = 65
        if self.mode == "bearing_failure":
            base += 0.05 * (self.t / 3600)
        return base + random.gauss(0, 0.5)

    def get_payload(self):
        vib = self.generate_vibration()
        temp = self.generate_temperature()
        payload = {
            "sensor_id": self.sensor_id,
            "timestamp": int(time.time()),
            "vibration": {
                "x": {"mean": vib[0], "std": 0.2, "rms": vib[0], "peak": vib[0]+0.5, "crest": 1.2},
                "y": {"mean": vib[1], "std": 0.2, "rms": vib[1], "peak": vib[1]+0.4, "crest": 1.18},
                "z": {"mean": vib[2], "std": 0.1, "rms": vib[2], "peak": vib[2]+0.3, "crest": 1.15}
            },
            "temperature": {"mean": temp, "std": 0.3, "rms": temp, "peak": temp+0.5, "crest": 1.01},
            "metadata": {"drive_type": "VDF", "rpm": self.rpm, "power_hp": 50}
        }
        self.t += 10
        return payload

# Publicar en MQTT
client = mqtt.Client()
client.connect("localhost", 1883, 60)

simulator = LHSensorSimulator("MOTOR-01", mode="bearing_failure")

while True:
    payload = simulator.get_payload()
    client.publish("sensors/simulated/data", json.dumps(payload))
    print(f"Enviado: {payload['sensor_id']} - VibZ: {payload['vibration']['z']['rms']:.2f} mm/s")
    time.sleep(10)  # Cada 10 segundos