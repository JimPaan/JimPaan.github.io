from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
import requests
from django.http import JsonResponse
import random

# Create your views here.


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('admin/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    return render(request, 'login.html')


def route(request):
    my_headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9hcGkudW0uZWR1Lm15Iiwic3ViIjoiMzExNTkyYWYtMWY0NC01MDMyLThiYjQtNGFjNzYzZGFlOWFmIiwiaWF0IjoxNTQ1NjM0OTMzLCJleHAiOjE2MzE5NDg1MzMsIm5hbWUiOiJ2ZWhpY2xlIn0.-EwaMdzZyILuKZ7Mjuemm4hvQM-H5kcza1dTle3nsWs'
    }
    response = requests.get('https://api.um.edu.my/vehicle/route', headers=my_headers)
    data = response.json()

    context = {
        'data': data,
    }
    return render(request, 'Test.html', context)


def bus_stop(request, pk):
    my_headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9hcGkudW0uZWR1Lm15Iiwic3ViIjoiMzExNTkyYWYtMWY0NC01MDMyLThiYjQtNGFjNzYzZGFlOWFmIiwiaWF0IjoxNTQ1NjM0OTMzLCJleHAiOjE2MzE5NDg1MzMsIm5hbWUiOiJ2ZWhpY2xlIn0.-EwaMdzZyILuKZ7Mjuemm4hvQM-H5kcza1dTle3nsWs'
    }
    response = requests.get('https://api.um.edu.my/vehicle/route/'+pk, headers=my_headers)
    data = response.json()
    locations = []

    for item in data['stops']:
        locations.append(
            {'stop_id': item['stop_id'],
             'name': item['name'],
             'latitude': item['lat'],
             'longitude': item['long'],
             'url': 'http://127.0.0.1:8000/rtbl/'+data['route_id']+'/'+item['stop_id']
             }
        )

    context = {
        'locations': locations,
    }
    return render(request, 'stops.html', context)


def rtbl(request, pk, pt):
    my_headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9hcGkudW0uZWR1Lm15Iiwic3ViIjoiMzExNTkyYWYtMWY0NC01MDMyLThiYjQtNGFjNzYzZGFlOWFmIiwiaWF0IjoxNTQ1NjM0OTMzLCJleHAiOjE2MzE5NDg1MzMsIm5hbWUiOiJ2ZWhpY2xlIn0.-EwaMdzZyILuKZ7Mjuemm4hvQM-H5kcza1dTle3nsWs'
    }
    response = requests.get('https://api.um.edu.my/vehicle/route/'+pk, headers=my_headers)
    data = response.json()
    locations = []
    user_info = [
        {
            'route_id': pk,
            'stop_id': pt,
        }
    ]

    for item in data['stops']:
        if item['stop_id'] == pt:
            locations.append(
                {
                    'latitude': item['lat'],
                    'longitude': item['long'],
                }
            )

    context = {
        'locations': locations,
        'user_info': user_info,
    }

    return render(request, 'buslocation.html', context)


def get_buslocation(request, pk, pt):
    my_headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9hcGkudW0uZWR1Lm15Iiwic3ViIjoiMzExNTkyYWYtMWY0NC01MDMyLThiYjQtNGFjNzYzZGFlOWFmIiwiaWF0IjoxNTQ1NjM0OTMzLCJleHAiOjE2MzE5NDg1MzMsIm5hbWUiOiJ2ZWhpY2xlIn0.-EwaMdzZyILuKZ7Mjuemm4hvQM-H5kcza1dTle3nsWs'
    }
    response = requests.get('https://api.um.edu.my/vehicle/bus/' + pk + '/' + pt, headers=my_headers)
    data = response.json()
    bus_location = []
    i = 2
    for item in data:
        bus_location.append(
            {
                'latitude': item['position']['latitude'],
                'longitude': item['position']['longitude'],
                'eta': item['eta']['time'],
                'distance': item['eta']['distance'],
                'Next_station': item['nextStop']['name'],
                'plate_no': item['bus']['plate_no'],
                'color': random_color(i),
            }
        )
        i += 1
    context = {
        'bus_location': bus_location,
    }

    return JsonResponse(context)


def random_color(i):
    color = ['red', 'yellow', 'green', 'purple']
    return color[i]
