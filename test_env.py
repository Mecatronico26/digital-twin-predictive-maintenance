import sys
print(f"Python: {sys.version}")

# ✅ IMPORTA EL PAQUETE RAÍZ PARA LA VERSIÓN
import paho.mqtt as mqtt  # <-- Aquí está __version__
# ✅ IMPORTA EL SUBMÓDULO CLIENT PARA FUNCIONALIDAD
import paho.mqtt.client as mqtt_client

import numpy as np
from scipy.fft import rfft

print("✅ Entorno virtual configurado correctamente.")
print(f"✅ MQTT: {mqtt.__version__}")  # <-- Ahora funciona
print(f"✅ NumPy: {np.__version__}")
print(f"✅ SciPy FFT disponible.")

# ✅ Prueba opcional: crea un cliente MQTT (sin conectar)
try:
    client = mqtt_client.Client()
    print("✅ Cliente MQTT creado correctamente.")
except Exception as e:
    print(f"❌ Error al crear cliente MQTT: {e}")