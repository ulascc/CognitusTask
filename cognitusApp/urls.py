from django.urls import path
from .views import DataView, TraineView, PredictView, LogView
from django.views.generic import TemplateView

urlpatterns = [
    path('dataworkspace/', DataView.as_view(), name='dataAPI'),
    path('dataPage/', TemplateView.as_view(template_name='index.html'), name='dataPage'),

    path('predictPage/', TemplateView.as_view(template_name='predict.html'), name='predictPage'),
    path('datapredict/', PredictView.as_view(), name='datapredict'),

    path('trainePage/', TemplateView.as_view(template_name='traine.html'), name='trainePage'),
    path('datatraine/', TraineView.as_view(), name='datatraine'),

    path('trainelogs/', LogView.as_view(), name='trainelogs'),
]