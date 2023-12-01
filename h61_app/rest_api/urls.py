# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet, DeviceDataViewSet, AlarmViewSet, CommandViewSet,VariableViewSet,DeviceDataByVariableView

router = DefaultRouter()
router.register(r'devices', DeviceViewSet)
router.register(r'data', DeviceDataViewSet)
router.register(r'alarms', AlarmViewSet)
router.register(r'commands', CommandViewSet, basename='command')
router.register(r'variable', VariableViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('device/<int:device_id>/variable/<str:variable_name>/data/', DeviceDataByVariableView.as_view(), name='device-variable-data'),

]
