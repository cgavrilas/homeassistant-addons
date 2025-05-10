import subprocess
import paho.mqtt.client as mqtt
import time

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
TOPIC_PUBLISH = "voltronic/raw"
TOPIC_COMMAND = "voltronic/cmd"
PORT = "/dev/ttyS0"
PROTOCOL = "PI41"

client = mqtt.Client()

def trimite(topic, payload):
    client.publish(topic, payload)

def executa_comanda(cmd):
    try:
        rezultat = subprocess.run(["mppsolar", "-p", PORT, "-P", PROTOCOL, "-c", cmd],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return rezultat.stdout.strip()
    except Exception as e:
        return f"Err: {e}"

def on_message(client, userdata, msg):
    comanda = msg.payload.decode()
    raspuns = executa_comanda(comanda)
    trimite(TOPIC_PUBLISH, raspuns)

def main():
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.subscribe(TOPIC_COMMAND)
    client.loop_start()

    while True:
        rezultat = executa_comanda("QPIGS")
        if rezultat:
            trimite(TOPIC_PUBLISH, rezultat)
        time.sleep(10)

if __name__ == "__main__":
    main()
