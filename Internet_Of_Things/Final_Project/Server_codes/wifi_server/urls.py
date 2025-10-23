from django.urls import include, path
from . import views

urlpatterns = [
    path('index/', views.index, name="index"),
    path('index2/', views.index2, name="index2"),
    path('on/', views.turn_led_on, name="turn_on"),
    path('off/', views.turn_led_off, name="turn_off"),
    path('status/', views.get_led_status, name="status"),
    path('telegram/', views.get_led_telegram_status, name="telegram"),
    path('timing/', views.get_timing_values, name="timing"),
]