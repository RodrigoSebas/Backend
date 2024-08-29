from rest_framework.decorators import (api_view, 
                                       permission_classes)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import (Usuario, 
                     ListaNovio,
                     Regalo)
from .serializers import (RegistroSerializer,
                          UsuarioSerializer,
                          ListaNoviosCreacionSerializer,
                          ListaNovioSerializer,
                          RegaloSerializer)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

    
)

from .permissions import EsAdministrador, EsNovio

from django.db import transaction

from cloudinary import utils
from os import environ

from datetime import datetime
from django.db.models import Q


@api_view(http_method_names=['POST'])
def crearUsuario(request):

    body = request.data
    serializador = RegistroSerializer(data=body)

    if serializador.is_valid():
        nuevo_usuario = Usuario(nombre = serializador.validated_data['nombre'],
                apellido = serializador.validated_data['apellido'],
                correo = serializador.validated_data['correo'],
                numeroTelefonico = serializador.validated_data['numeroTelefonico'],
                tipoUsuario = serializador.validated_data['tipoUsuario'])
        
        nuevo_usuario.set_password(serializador.validated_data['password'])
        
        if serializador.validated_data['tipoUsuario'] == 'ADMIN':
            nuevo_usuario.is_superuser = True
        
        nuevo_usuario.save()
        
        return Response(data={
            'message': 'Usuario creado exitosamente'
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(data={
            'message':'Error al crear el usuario',
            'content':serializador.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def perfilUsuario(request):
    #print(request.user.nombre)
    #cuando queremos pasar una instancia a nuestro serializador usaremos el parametro instance
    #, sin embargo si queremos pasarle informacion que lo valide usaremos el parametro
    #data

    #cuando trae la info del base de datos para validarla se usa instance
    #cuando viene del frontend la data se usa data
    serializador = UsuarioSerializer(instance=request.user)

    return Response(data={
        'message':'',
        'content': serializador.data
    })


class ListaNoviosAPIView(APIView):
    #en esta lista el orden importa, pues ejecutara primero isauthenticated luego esadministrador
    permission_classes = [IsAuthenticated, EsAdministrador]
    def post(self, request):
        serializador = ListaNoviosCreacionSerializer(data = request.data)
        if serializador.is_valid():
            with transaction.atomic():
                # todo lo que hagamos tiene que completarse exitosamente, si algo falla entonces todas las inserciones, actualizaciones y eliminaciones quedaran sin efecto
                nuevoNovio = Usuario(nombre=serializador.validated_data.get('novio').get('nombre'),
                                     apellido=serializador.validated_data.get(
                                         'novio').get('apellido'),
                                     correo=serializador.validated_data.get(
                                         'novio').get('correo'),
                                     tipoUsuario='NOVIO',
                                     numeroTelefonico=serializador.validated_data.get('novio').get('numeroTelefonico'))

                nuevoNovio.set_password(
                    serializador.validated_data.get('novio').get('password'))

                nuevoNovia = Usuario(nombre=serializador.validated_data.get('novia').get('nombre'),
                                     apellido=serializador.validated_data.get(
                                         'novia').get('apellido'),
                                     correo=serializador.validated_data.get(
                                         'novia').get('correo'),
                                     numeroTelefonico=serializador.validated_data.get(
                                         'novia').get('numeroTelefonico'),
                                     tipoUsuario='NOVIO')

                nuevoNovia.set_password(
                    serializador.validated_data.get('novia').get('password'))

                nuevoNovio.save()
                nuevoNovia.save()

                nuevaLista = ListaNovio(
                    novio=nuevoNovio, novia=nuevoNovia)
                nuevaLista.save()
            return Response(data={
                'message':'lista creada exitosamente'
        }, status=status.HTTP_201_CREATED)

        else:
            return Response(data={
                'message':'Error al crear la lista de novios',
                'content': serializador.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
    
    def get(self,request):
        resultado = ListaNovio.objects.all()
        #si al parametro instance le vamos a pasar una lista
        #entonces se usa many
        serializador = ListaNovioSerializer(instance=resultado, many=True)

        
        return Response(data={
            'content':serializador.data
        })
    

class RegalosAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, EsNovio]

    def post(self, request):
        # TAREA!
        # Crear un serializador para obtener la informacion de crear un regalo
        # en el campo de la imagen enviar la url que cloudinary nos brinda (la segura)
        # Solamente LOS NOVIOS PUEDEN agregar regalos y buscar la lista de novios del novio o novia en la cual se quiere agregar el regalo
        print(request.user)
        # SELECT * FROM lista_novios WHERE novio_id = '...' OR novia_id = '...';
        listaEncontrada = ListaNovio.objects.filter(
            Q(novio=request.user) | Q(novia=request.user)).first()

        if not listaEncontrada:
            return Response(data={
                'message':'El novio/a no tiene aun una lista creada, comuniquese con el administrador'
            }, status=status.HTTP_400_BAD_REQUEST)
        print(listaEncontrada)

        #ahora agregamos el registro de nuestra lista novios al body para pasarlo por el serializador
        request.data['listaNovio'] = listaEncontrada.id

        serializador = RegaloSerializer(data=request.data)
        if serializador.is_valid():
            serializador.save()

            return Response(data={
                'message': 'Regalo creado exitosamente',
                'content':serializador.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                'message': 'Hubo un error ',
                'content': serializador.errors
            })

    def get(self, request):
        # Retornar todos los regalos del novio que actualmente esta logeado

        # SELECT * FROM lista_novios WHERE novio_id = 1 LIMIT 1 ;
        listNovioEncontrado = ListaNovio.objects.filter(novio=1).first()
        regalos = Regalo.objects.filter(
            listaNovio=listNovioEncontrado.id).all()

        return Response(data={
            'message': ''
        })
    

@api_view(http_method_names=['POST'])
def generarCloudinaryUrl(request):
    timestamp = datetime.now().timestamp()
    signature = utils.api_sign_request(
        {'timestamp': timestamp}, environ.get('CLOUDINARY_API_SECRET'))

    url = f"https://api.cloudinary.com/v1_1/{environ.get('CLOUDINARY_NAME')}/image/upload?api_key={environ.get('CLOUDINARY_API_KEY')}&timestamp={timestamp}&signature={signature}"
    
    return Response({
        'content': url
    })