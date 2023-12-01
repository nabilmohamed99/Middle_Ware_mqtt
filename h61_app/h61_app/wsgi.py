import os
from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'h61_app.settings')

application = get_wsgi_application()


from rest_api.middleware import MqttMiddleware  
mqtt_middleware = MqttMiddleware()
mqtt_middleware.start()
