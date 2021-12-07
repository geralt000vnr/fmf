import string
import random
from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.

from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
import base64
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.authentication import get_authorization_header
from rest_framework import HTTP_HEADER_ENCODING
from .models import *
from .serializers import *


def authorized(request):
    auth = get_authorization_header(request).split()
    if not auth or auth[0].lower() != b'basic':
        msg = _("Not basic authentication.")
        result = {'status': False, 'message': msg}
        return result
    if len(auth) == 1:
        msg = _('Invalid basic header. No credentials provided.')
        result = {'status': False, 'message': msg}
        return result
    elif len(auth) > 2:
        msg = _('Invalid basic header. Credentials string should not contain spaces.')
        result = {'status': False, 'message': msg}
        return result
    try:
        auth_parts = base64.b64decode(auth[1]).decode(HTTP_HEADER_ENCODING).partition(':')
    except (TypeError, UnicodeDecodeError, binascii.Error):
        msg = _('Invalid basic header. Credentials not correctly base64 encoded.')
        result = {'status': False, 'message': msg}
        return result

    userid, password = auth_parts[0], auth_parts[2]
    # Your auth table specific codes
    if 'fmf' == userid and '026866326a9d1d2b23226e4e892919982g' == password:  # my dummy code
        result = {'status': True, 'message': ""}
        return result
    else:
        msg = _('User not found.')
        result = {'status': False, 'message': msg}
        return result


@csrf_exempt
def add_station(request):
    result = authorized(request)
    if result['status'] == True:
        try:
            if request.method == 'POST':
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                phone = request.POST.get('phone')
                email = request.POST.get('email')
                pin = request.POST.get('pin')
                name = request.POST.get('station_name')
                timing = request.POST.get('timing')
                address = request.POST.get('address')
                cng_available = request.POST.get('cng_available')
                image = request.FILES["image"]
                S = 10
                username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email,
                                                phone=phone, pin=pin, password="herk12354312")
                station = Stations.objects.create(vendor=user, name=name, timing=timing, address=address,
                                                  cng_available=cng_available,
                                                  image=image)
                return JsonResponse({'status': True, 'message': 'Station Added'})
        except Exception as e:
            return JsonResponse({'status': False, 'exception': str(e)})
    return JsonResponse({'status': False, 'message': 'Unauthorised User'})


@csrf_exempt
def vendor_login(request):
    result = authorized(request)
    if result['status'] == True:
        tok = MyTokenObtainPairSerializer()
        try:
            if request.method == "POST":
                phone = request.POST.get('phone')
                pin = request.POST.get('pin')
                try:
                    user = User.objects.filter(phone=phone, pin=pin)
                except:
                    user = None
                if user is not None:
                    station = Stations.objects.get(vendor=user)
                    sation_serailizer = StationSerializer(station)
                    token = tok.get_token(user)
                    stoken = str(token)
                    return JsonResponse({'status': True, 'data': sation_serailizer.data, 'token': stoken})
                return JsonResponse({'status': False, 'message': 'Wrong Credentials'})
        except Exception as e:
            return JsonResponse({'status': False, 'exception': str(e)})
    return JsonResponse({'status': False, 'message': 'Unauthorised User'})


def station_list(request):
    result = authorized(request)
    if result['status'] == True:
        if request.method == 'GET':
            station = Stations.objects.all()
            station_serializer = StationSerializer(station, many=True)
            return JsonResponse({'status': True, 'data': station_serializer.data})
    return JsonResponse({'status': False, 'message': 'Unauthorised User'})


@csrf_exempt
def chnage_cng_status(request):
    result = authorized(request)
    if result['status'] == True:
        try:
            if request.method == 'POST':
                id = request.POST.get('station_id')
                cng_available = request.POST.get('cng_available')
                Stations.objects.filter(id=id).update(cng_available=cng_available)
                return JsonResponse({'status': True, 'message': 'Status Changed'})
        except Exception as e:
            return JsonResponse({'status': False, 'exception': str(e)})
    return JsonResponse({'status': False, 'message': 'Unauthorised User'})
