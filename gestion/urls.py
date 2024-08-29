from django.urls import path
from .views import (crearUsuario, 
                    perfilUsuario,
                    ListaNoviosAPIView,
                    generarCloudinaryUrl,
                    RegalosAPIView)
from rest_framework_simplejwt.views import TokenObtainPairView
#no se pone as_view porque crearusuarioe es una funcion no una clase

urlpatterns = [
    path('registro', crearUsuario),
    path('login',TokenObtainPairView.as_view()),
    path('perfil', perfilUsuario),
    path('lista-novios', ListaNoviosAPIView.as_view()),
    path('cloudinary-url', generarCloudinaryUrl),
    path('regalos', RegalosAPIView.as_view() )
]