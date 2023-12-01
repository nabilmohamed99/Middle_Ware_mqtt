# views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Device, DeviceData, Alarm, Command,Variable
from .serializers import DeviceSerializer, DeviceDataSerializer, AlarmSerializer, CommandSerializer,VariableSerializer
import paho.mqtt.client as mqtt
from rest_framework import generics

class VariableViewSet(viewsets.ModelViewSet):
    queryset = Variable.objects.all()
    serializer_class = VariableSerializer
class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceDataViewSet(viewsets.ModelViewSet):
    queryset = DeviceData.objects.all()
    serializer_class = DeviceDataSerializer

class AlarmViewSet(viewsets.ModelViewSet):
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer

class CommandViewSet(viewsets.ModelViewSet):
    queryset = Command.objects.all()
    serializer_class = CommandSerializer

    @action(detail=False, methods=['post'])
    def send_command(self, request):
        # Vous recevez la commande ici
        command = request.data.get('command', '')
        device_id = request.data.get('device_id', None)

        if device_id is not None:
            # Vous pouvez traiter la commande et envoyer via MQTT
            # Assurez-vous que la logique de commande est sécurisée
            mqtt_topic = f"commands/{device_id}"
            message = {"command": command}
            mqtt.publish(mqtt_topic, payload=json.dumps(message), qos=0, retain=True)

            # Enregistrez la commande dans la base de données
            command_obj = Command(device_id=device_id, command=command)
            command_obj.save()

            return Response({'success': True})
        else:
            return Response({'success': False, 'message': 'Device ID is required for the command.'})
 

class DeviceDataByVariableView(generics.ListAPIView):
    serializer_class = DeviceDataSerializer

    def get_queryset(self):
        device_id = self.kwargs['device_id']
        variable_name = self.kwargs['variable_name']

        datetime_debut = self.request.query_params.get('datetime_debut')
        datetime_fin = self.request.query_params.get('datetime_fin')

        try:
            device = Device.objects.get(pk=device_id)
            variable = Variable.objects.get(name=variable_name)
        except Device.DoesNotExist:
        
            return DeviceData.objects.none()
        except Variable.DoesNotExist:
          
            return DeviceData.objects.none()

        queryset = DeviceData.objects.filter(device=device, variable=variable)

        if datetime_debut:
            queryset = queryset.filter(timestamp__gte=datetime_debut)

        if datetime_fin:
            queryset = queryset.filter(timestamp__lte=datetime_fin)

        return queryset