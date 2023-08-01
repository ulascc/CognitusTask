from django.contrib import admin
from django.urls import path, include
from cognitusApp.views import DataView

urlpatterns = [
    path('data/', include('cognitusApp.urls')),
]