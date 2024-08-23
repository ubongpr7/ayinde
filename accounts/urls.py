from django.urls import path
from .views import account



urlpatterns=[
    path('register/',account,name='register' ),
]

# path(route,view=, name=)