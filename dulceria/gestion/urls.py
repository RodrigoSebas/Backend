# aqui van las rutas de la app gestion
from django.urls import path
from .views import (paginaPrueba, 
                    CategoriasAPIView, 
                    CrearCategoriaAPIView,
                    CrearYListarCategoriaAPIView,
                    DevolverActualizarEliminarCategoriaAPIView,
                    GolosinasAPIView)


urlpatterns = [
    path('prueba', paginaPrueba),
    path('categorias', CategoriasAPIView.as_view()),
    path('crear-categoria', CrearCategoriaAPIView.as_view()),
    path('listar-crear-categoria', CrearYListarCategoriaAPIView.as_view()),
    #cuando usamos una vista generica se tiene que definir un parametro
    #si utilizamos lookup_field se puede cambiar a id si no se debe de poner pk
    path('categoria/<id>', DevolverActualizarEliminarCategoriaAPIView.as_view()),
    path('golosinas', GolosinasAPIView.as_view()),
]