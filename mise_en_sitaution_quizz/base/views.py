from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import requests
from .forms import ControllerForm
from .models import Controller

from django.http import JsonResponse
from .models import Device
from django.contrib import messages

@csrf_exempt
def update_device_ip(request):
    if request.method == 'POST':
        ip_address = request.POST.get('ip')
        # Update or create the device record with the new IP
        device, created = Device.objects.update_or_create(
            id=1, defaults={'ip_address': ip_address}
        )
        
        # Try to reach the ESP32 to check connectivity
        try:
            # Assume you have a '/ping' endpoint that just needs a simple GET request
            response = requests.get(f'http://{ip_address}/ping', timeout=5)  # 5-second timeout for the request
            
            if response.status_code == 200:
                connection_status = 'connected'
            else:
                connection_status = 'error'
        except requests.ConnectionError:
            connection_status = 'disconnected'
        except requests.Timeout:
            connection_status = 'timeout'
        except Exception as e:
            connection_status = f'failed: {str(e)}'

        # Return the IP address and connection status in the response
        return JsonResponse({
            'status': 'success',
            'ip': ip_address,
            'connection_status': connection_status
        })

    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def control_sensor(request, sensor_number):
    try:
        device = Device.objects.get(id=1)  # Assuming there is only one device
        ESP32_IP = device.ip_address
        url = f'http://{ESP32_IP}/status/sensor_{sensor_number}'

        response = requests.get(url)
        if response.status_code == 200:
            sensor_data = response.json()
            sensor_status = sensor_data['status']
            request.session[f'sensor_{sensor_number}_status'] = sensor_status
            print(sensor_status)
            return JsonResponse({'status': 'success', 'sensor_status': sensor_status})
        else:
            return JsonResponse({'status': 'error', 'message': 'Device not responding'}, status=500)
    except requests.RequestException as e:
        request.session['connection_status'] = 'disconnected'
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

  
@csrf_exempt
def control_door(request, door_number, action):
    try:
        device = Device.objects.get(id=1)  # Assuming there is only one device configuration
        ESP32_IP = device.ip_address
        url = f'http://{ESP32_IP}/action/door_{door_number}/{action}'
        request.session['connection_status'] = 'connected'

        response = requests.get(url)
        if response.status_code == 200:
            request.session[f'door_{door_number}_status'] = 'ouverte' if action == 'open' else 'fermée'
            return JsonResponse({'status': 'success', 'message': f'Door {door_number} {action}'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Device not responding'}, status=500)
    except requests.RequestException as e:
        request.session['connection_status'] = 'disconnected'
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def home(request):
  door_1_status = request.session.get('door_1_status', 'inconnu')
  door_2_status = request.session.get('door_2_status', 'inconnu')
  door_3_status = request.session.get('door_3_status', 'inconnu')
  door_4_status = request.session.get('door_4_status', 'inconnu')
  sensor_1_status = request.session.get('sensor_1_status', 'inconnu')
  sensor_2_status = request.session.get('sensor_2_status', 'inconnu')
  sensor_3_status = request.session.get('sensor_3_status', 'inconnu')
  sensor_4_status = request.session.get('sensor_4_status', 'inconnu')
  controllers = Controller.objects.all()
  return render(request, "home.html", {
      'door_1_status': door_1_status,
      'door_2_status': door_2_status,
      'door_3_status': door_3_status,
      'door_4_status': door_4_status,
      'sensor_1_status': sensor_1_status,
      'sensor_2_status': sensor_2_status,
      'sensor_3_status': sensor_3_status,
      'sensor_4_status': sensor_4_status,
      'controllers': controllers,
      })

@login_required
def controller_create(request):
    if request.method == 'POST':
        form = ControllerForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('base:home')
            return HttpResponseRedirect('/#configuration')
        else:
            print(form.errors)
    else:
        form = ControllerForm()
    return render(request, 'components/crud_controller.html', {'form': form})

@login_required
def controller_delete(request, id):
    controller = get_object_or_404(Controller, id=id)
    controller.delete()
    # return redirect('base:home')
    return HttpResponseRedirect('/#configuration')

@login_required
def controller_edit(request, pk):
    controller = get_object_or_404(Controller, pk=pk)
    if request.method == 'POST':
        form = ControllerForm(request.POST, instance=controller)
        if form.is_valid():
            form.save()
            return redirect('base:home')
    else:
        form = ControllerForm(instance=controller)
    return render(request, 'components/crud_controller.html', {'form': form})

def authView(request):
 if request.method == "POST":
  form = UserCreationForm(request.POST or None)
  if form.is_valid():
   form.save()
   return redirect("base:login")
 else:
  form = UserCreationForm()
 return render(request, "registration/signup.html", {"form": form})


async def video_stream(websocket, path):
    while True:
        # Recevoir les données d'image du client
        image_data = await websocket.recv()

def video_feed(request):
    # Démarrez le serveur WebSocket dans un thread séparé
    start_websocket_server()
    return HttpResponse("WebSocket server started for video stream.")

def start_websocket_server():
    # Démarrer le serveur WebSocket
    start_server = websockets.serve(video_stream, 'localhost', 8000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()