from django.urls import path
from .views import create_profile, register,user_login



urlpatterns=[
    path('register/',register,name='register' ),
    path('create-profile/<str:id>/<str:role>/', create_profile, name='create_profile'),
    path('login/', user_login, name='login'),
    
]

# path(route,view=, name=)