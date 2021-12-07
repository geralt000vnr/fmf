from django.urls import path
from . import views

urlpatterns = [
    path('add_station/', views.add_station, name='Add Station'),
    path('vendor_login/', views.vendor_login, name='vendor_login'),
    path('station_list/', views.station_list, name='station_list'),
    path('chnage_cng_status/', views.chnage_cng_status, name='chnage_cng_status'),
]
