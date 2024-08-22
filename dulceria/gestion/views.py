from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (CreateAPIView,
                                     ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from .models import Categoria, Golosina
from .serializers import CategoriaSerializer, GolosinaSerializer
from rest_framework import status


def paginaPrueba(request):
    print(request)
    data = [{
        'id':1,
        'nombre':'Importados',
        'habilitado':True
    }, {
        "id":2,
        'nombre':'Nacionales',
        'habilitado':False
    }]

    usuario = 'Eduardo'

    return render(request, 'prueba.html', {"data":data,
                                           "usuario":usuario})

class CategoriasAPIView(APIView):
    def get(self, request):
        return Response(data={
            'message':'ok'
        }, status=200)
    
    def post(self, request):
        return Response(data={
            'message':'me hiciste post'
        }, status=200)
    
class CrearCategoriaAPIView(CreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class CrearYListarCategoriaAPIView(ListCreateAPIView):
    queryset = Categoria.objects.all()

    serializer_class = CategoriaSerializer

class DevolverActualizarEliminarCategoriaAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    # si queremos cambiar el valor del parametro por la url de pk a uno personalizado usaremos
    # el atributo lookup_field
    lookup_field = 'id'


# Create your views here.

class GolosinasAPIView(APIView):
    def post(self, request):
        data = request.data
        serializador = GolosinaSerializer(data=data)
        #hace la validadcion de los campos del body
        validacion = serializador.is_valid()

        if validacion:

            #se puede guardar el serializador en la base de datos
            #nuevaGolosina = serializador.save()

            #esto hace lo mismo que todo lo demas, guarda la nueva golosina en ela base de datos
            #Golosina(nombre = serializador.validated_data.get('nombre'),
                     #nombre = serializador.validated_data.get('precio'),
                     #nombre = serializador.validated_data.get('habilitado'),
                     #nombre = serializador.validated_data.get('categoria'))

            nuevaGolosina = Golosina(**serializador.validated_data)
            nuevaGolosina.save()

            #si queremos validar que la informacion a guadar o actualizar es correcta utilizaremos el parametro data,
            #caso contrario si queremos un diccionario osea deserializar usamos instance
            resultado = GolosinaSerializer(instance = nuevaGolosina)
            return Response(data = {
                'message':"Golosina creada exitosamente",
                'content':resultado.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                'message': 'Error al crear la golosina',
                'content':serializador.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
