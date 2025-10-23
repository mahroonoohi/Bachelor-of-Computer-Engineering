from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
import os
# Create your views here.


def index(request):
    context = {
        'turn_on_url': reverse("turn_on"),
        'turn_off_url': reverse("turn_off"),
        'get_status': reverse('status')
    }
    return render(request, 'wifi_server/index.html', context)



def turn_led_on(request):
    settings.LED_STATUS = 1
    print(f"***************************** {settings.LED_STATUS}")
    return HttpResponseRedirect(reverse("index"))



def turn_led_off(request):
    settings.LED_STATUS = 0
    print(f"***************************** {settings.LED_STATUS}")
    return HttpResponseRedirect(reverse("index"))



def get_led_status(request):
    print(f"***************************** {settings.LED_STATUS}")
    if settings.LED_STATUS:
        return HttpResponse(status=250)
    
    else:
        return HttpResponse(status=251)



def index2(request):
    if request.GET:
        on_value = int(request.GET.get('on'))
        off_value = int(request.GET.get('off'))

        settings.LED_ON_TIME = on_value
        settings.LED_OFF_TIME = off_value

        print(f"***************************** on time {settings.LED_ON_TIME}")
        print(f"***************************** off time {settings.LED_OFF_TIME}")

    return render(request, 'wifi_server/index2.html')



def get_timing_values(request):
    return HttpResponse(f"{settings.LED_ON_TIME}&{settings.LED_OFF_TIME}")



def get_led_telegram_status(request):
    with open(os.path.join(settings.BASE_DIR, 'led.txt'), 'r') as file:
        first_line = file.readline().strip()
        if first_line == "0":
            return HttpResponse(status=251)
        elif first_line == "1":
            return HttpResponse(status=250)
        else:
            raise ValueError("invalid led status!")
