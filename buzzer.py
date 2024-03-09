from gpiozero import Buzzer
import paho.mqtt.client as mqtt
from flask import Flask, request
from flask_cors import CORS
from twilio.rest import Client

app = Flask(__name__)
CORS(app)

MQTT_BROKER = 'mqtt-dashboard.com'
MQTT_PORT = 1883
MQTT_TOPIC_ON = 'sensor/alarm'

buzzer = Buzzer(17)

TWILIO_SID = 'AC2af985f16f1065e40cd8274f88b0978b'
TWILIO_AUTH_TOKEN = 'e7851945fff078ab6ff9129f2090348d'
FROM_WHATSAPP_NUMBER = 'whatsapp:+14155238886'
TO_WHATSAPP_NUMBER = 'whatsapp:+558197512509'
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def send_whatsapp_message(message):
    try:
        client.messages.create(
            body=message,
            from_=FROM_WHATSAPP_NUMBER,
            to=TO_WHATSAPP_NUMBER
        )
        print("WhatsApp message sent successfully")
    except Exception as e:
        print("Error sending WhatsApp message:", e)


def on_message(client, userdata, msg):
 if msg.topic == MQTT_TOPIC_ON:
  buzzer.beep()
  send_whatsapp_message("Alarm activated!")

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

@app.route('/start-script', methods=['GET'])
def start_script():
 mqtt_client.subscribe(MQTT_TOPIC_ON)
 return 'Script started'

@app.route('/stop-script', methods=['GET'])
def stop_script():
 buzzer.off()
 mqtt_client.unsubscribe(MQTT_TOPIC_ON)
 send_whatsapp_message("Alarm desactivated!")
 return 'Script stopped'

if __name__ == '__main__':
 app.run(port=5000)