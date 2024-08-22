from rest_framework.serializers import ModelSerializer
from .models import Categoria, Golosina

class CategoriaSerializer(ModelSerializer):
    class Meta:
        model = Categoria
        #especificar que atributos vamos a utilizar

        # fields = ['id', 'nombre']
        #si queremos utilizar todos los atributos
        fields = '__all__'

        #si queremos utilizar la mayoria de los atributos pero obviar algunos
        #exclude = ['id']

        #no se puede utilizar el fields y el exclude al mismo tiempo


class GolosinaSerializer(ModelSerializer):
    class Meta:
        model = Golosina
        fields = '__all__'