import paho.mqtt.client as mqtt
import json

# Thông tin kết nối MQTT
mqtt_broker_address = "mqtt.thingspeak.com"
mqtt_username = "your_mqtt_username"
mqtt_password = "your_mqtt_password"

mqtt_topic_humidity = "channels/your_channel_id/subscribe/json/field1/your_api_key"
mqtt_topic_temperature = "channels/your_channel_id/subscribe/json/field2/your_api_key"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe([(mqtt_topic_humidity, 0), (mqtt_topic_temperature, 0)])

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        humi = data.get("field1", 0)
        temp = data.get("field2", 0)
        print("HUMI : {}%".format(humi))
        print("TEMP : {}°C".format(temp))

    except :
        print("Error processing MQTT message:", str(e))

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_address, 1883, 60)

while True:
    try:
        client.loop_forever()
    except Exception as e:
        print("Failed to connect to MQTT broker:", str(e))