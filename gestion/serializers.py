from rest_framework import serializers
from .models import Usuario, ListaNovio, Regalo

# ModelSerializer > sirve para crear un serializador pero basandonos en un
# modelo de nuestro Models, es decir, utilizara todos los atributos
# del modelo para hacer las validaciones

# Serializer > crear un serializador pero sin la necesidad de basarse
#en un model(tabla) sino que completamente modificable
# y no tendra como base un modelo

class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        #fields = '__all__'
        exclude = ['password', 'is_staff', 'is_superuser','is_active',
                   'groups', 'user_permissions']
        
        #sirve para agregar configuracion adicional a los atributos de la clase
        extra_kwargs = {
            'last_login':{'write_only':True}
        }

class NovioSerializer(serializers.Serializer):
    nombre = serializers.CharField(required=True)
    apellido = serializers.CharField(required=True)
    correo = serializers.EmailField(required=True)
    numeroTelefonico = serializers.CharField(required=True)
    password = serializers.CharField()


class ListaNoviosCreacionSerializer(serializers.Serializer):
    novio = NovioSerializer(required=True)
    novia = NovioSerializer(required=True)

class ListaNovioSerializer(serializers.ModelSerializer):
    #si queremos definir atributos a mostrar (no todos) de los modelos anidados

    novio = UsuarioSerializer()
    novia = UsuarioSerializer()

    #sai queremos usar otro nombre de varible se usa source
    #lanovia = UsuarioSerializer(source='novia')
    class Meta:
        model = ListaNovio
        fields = '__all__'
        #si en nuestro modelo actual tenemos llaves foraneas podemos 
        #acceder a su informacion adyacente mediante la profundidad, en base
        #al numero que pongamos ingresaremos a cuantos vecinos tengamos
        #lista_novios(novio_id) > novios(ciudad_id) > ciudades(pais_id) paises
        #depth = 1
        #ingresara la lista novios y a los novios
        #depth = 2
        #ingresara la lista novios, a los novios y ciudades
        #depth = 3
        #ingresara la lista novios, a los novios, ciudades y al pais
       # depth = 1

class RegaloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regalo
        fields = '__all__'
