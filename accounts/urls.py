from django.urls import path
from .views import create_profile, register,user_login,signout



urlpatterns=[
    path('register/',register,name='register' ),
    path('create-profile/<str:id>/<str:role>/', create_profile, name='create_profile'),
    path('login/', user_login, name='login'),
    path('signout/', signout, name='signout'),
    
]

# path(route,view=, name=)