from gpiozero import Buzzer
import paho.mqtt.client as mqtt
from flask import Flask, request
from flask_cors import CORS
from twilio.rest import Client
import requests

app = Flask(__name__)
CORS(app)

MQTT_BROKER = 'mqtt-dashboard.com'
MQTT_PORT = 1883
MQTT_TOPIC_ON = 'sensor/alarm'

buzzer = Buzzer(17)

TWILIO_SID = 'AC2af985f16f1065e40cd8274f88b0978b'
TWILIO_AUTH_TOKEN = 'b7e37cf9618bf0d455ed01a3dc8fabbf'
FROM_WHATSAPP_NUMBER = 'whatsapp:+14155238886'
TO_WHATSAPP_NUMBER = ''
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def send_whatsapp_message(message):
    if TO_WHATSAPP_NUMBER == '':
        print('No cellphone number')
        return
    try:
        print(TO_WHATSAPP_NUMBER)
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
  send_thing_alarm(1)
  send_whatsapp_message("Alarm activated!")

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

@app.route('/start-script', methods=['POST'])
def start_script():
 global TO_WHATSAPP_NUMBER

 data = request.json
 TO_WHATSAPP_NUMBER = 'whatsapp:+55' + str(data.get('cellphone'))
 mqtt_client.subscribe(MQTT_TOPIC_ON)
 send_thing_is_actived_alarm(1)
 return 'Script started'

@app.route('/stop-script', methods=['GET'])
def stop_script():
 buzzer.off()
 mqtt_client.unsubscribe(MQTT_TOPIC_ON)
 send_thing_is_actived_alarm(0)
 send_whatsapp_message("Alarm desactivated!")
 return 'Script stopped'

def send_thing_is_actived_alarm(is_activated):
 url = 'https://api.thingspeak.com/update?api_key=HS9984TRRZWDIMCA&field1='+str(is_activated)
 response = requests.get(url)
 if response.status_code == 200:
  print(response.text)
 else:
  print('Error:', response.status_code)

def send_thing_alarm(last_alarm):
 url = 'https://api.thingspeak.com/update?api_key=HS9984TRRZWDIMCA&field2='+str(last_alarm)
 response = requests.get(url)
 if response.status_code == 200:
  print('sent last alarm')
  print(response.text)
 else:
  print('Error:', response.status_code)

if __name__ == '__main__':
 app.run(port=5000)