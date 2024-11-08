#!/usr/bin/python
import random
import time
import json
import paho.mqtt.client as mqtt

# Inställningar för MQTT
MQTT_BROKER = "lynx.iotopen.se"  # Ändra till rätt broker-adress för IoT-Open
MQTT_PORT = 8883  # Standardport för MQTT över TLS
MQTT_TOPIC = "0000/obj/simulate/temperature"  # Lägg till clientID och rätt topic_read från din "funktion"

# Autentiseringsuppgifter
MQTT_USER = "random"  # Lägg till rätt användarnamn
MQTT_PASSWORD = "DINA_API-Keys"   # Lägg till rätt API-keys

# Skapa MQTT-klient och anslutningsinställningar
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

# Aktivera TLS/SSL
client.tls_set()  # Om certifikat behövs kan du lägga till dem som argument här

# Anslut till MQTT-brokern
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
except Exception as e:
    print(f"Kunde inte ansluta till MQTT-brokern: {e}")

def simulate_temperature():
    """Genererar ett slumpmässigt temperaturvärde mellan 20 och 25 grader Celsius."""
    return round(random.uniform(20, 25), 2)

try:
    while True:
        # Simulera temperaturvärde
        temperature = simulate_temperature()
        # Skapa ett JSON-meddelande
        payload = json.dumps({"value": temperature})
        # Skicka meddelandet till MQTT-topic
        client.publish(MQTT_TOPIC, payload)
        print(f"Skickade temperatur: {temperature}°C")
        
        # Vänta 5 sekunder innan nästa mätning
        time.sleep(5)

except KeyboardInterrupt:
    print("Avslutar simulering...")
finally:
    client.disconnect()
