from django.urls import path
from .views import *
urlpatterns=[
    path('',home,name='home'),
    path('update/<str:app_name>/<str:model_name>/<int:pk>/', GenericUpdateView.as_view(), name='generic_update'),
    path('add/<str:app_name>/<str:model_name>/', GenericCreateView.as_view(), name='generic_create'),
]