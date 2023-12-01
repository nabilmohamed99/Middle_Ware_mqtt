# middleware.py
import json
import paho.mqtt.client as mqtt
from .models import DeviceData, Alarm, Command, Device, Variable

MQTT_BROKER = "y77a91e8.emqx.cloud"
MQTT_PORT = 1883
class MqttMiddleware:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        self.client.username_pw_set("meier", password="123")
        self.client.connect("y77a91e8.emqx.cloud", 1883, 60)
        self.start()


    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
      
        client.subscribe("data/#")
        client.subscribe("devices/#")
        # client.subscribe("commands/#")

    def on_message(self, client, userdata, msg):
        print("Erreeeur")
        payload = json.loads(msg.payload)
        print(payload)
        topic_parts,id = msg.topic.split("/")
        print( topic_parts, id)
        
        if topic_parts == "devices":
            self.process_data(payload,id)
        elif topic_parts == "alarms":
            self.process_alarm(payload)
        

    def process_data(self, data, id):
        try:
            print(f"Processing data for device {id}: {data}")
            device = Device.objects.get(pk=id)
            
            for variable_name, value in data.items():
                print(f"Processing variable {variable_name} with value {value}")
                if variable_name == "id":
                    continue

                variable = Variable.objects.get(name=variable_name)
                device_data_instance = DeviceData(device=device, variable=variable, value=value)
                device_data_instance.save()
                print(f"Saved data for variable {variable_name} of device {id}")
        except Exception as e:
            print(f"Error processing data for device {id}: {e}")


                

    def process_alarm(self, alarm):
        # Enregistrez les alarmes dans la base de données
        device_id = alarm.get('device_id')
        message = alarm.get('message')
        alarm = Alarm(device_id=device_id, message=message)
        alarm.save()

    def process_command(self, command):
        # Traitez les commandes reçues depuis MQTT
        device_id = command.get('device_id')
        command_value = command.get('command')
       
        confirmation_topic = f"commands/{device_id}/confirmation"
        self.client.publish(confirmation_topic, payload="Command received", qos=0, retain=False)

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
