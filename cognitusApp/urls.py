from django.urls import path
from .views import DataView
from django.views.generic import TemplateView

urlpatterns = [
    path('dataworkspace/', DataView.as_view(), name='dataAPI'),
    path('dataPage/', TemplateView.as_view(template_name='index.html'), name='dataPage'),
    path('predictPage/', TemplateView.as_view(template_name='predict.html'), name='predictPage'),
]