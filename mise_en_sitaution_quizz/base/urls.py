from django.urls import path, include
from .views import home, controller_create, update_device_ip, control_door, control_sensor, authView, controller_delete, controller_edit, video_feed

urlpatterns = [
    path("", home, name="home"),
    path('api/update_ip', update_device_ip, name='update_ip'),
    path('controller/create/', controller_create, name='controller_create'),
    path('controller/delete/<int:id>/', controller_delete, name='controller_delete'),
    path('controller/edit/<int:pk>/', controller_edit, name='controller_edit'),
    path('action/door_<int:door_number>/<str:action>/', control_door, name='control_door'),
    path('status/sensor_<int:sensor_number>/', control_sensor, name='control_sensor'),
    path("signup/", authView, name="authView"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('video_feed/', video_feed, name='video_feed'),
]
