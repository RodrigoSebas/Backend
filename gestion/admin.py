from django.contrib import admin
from .models import Usuario

# Register your models here.

class UsuarioAdmin(admin.ModelAdmin):
    #mensaje en caso en una columna no haya valor
    empty_value_display = 'NO HAY'

    #como queremos mostrar los registros del modelo
    list_display = ['nombre', 'apellido', 'correo']
    
    #lista de atributos en las cuales queremos excluir para
    # ya sea crear o actualizar nuestro registro
    exclude = ['nombre']
    
    #sirve para indicar en que columnas yo puedo selecionar al usuario para ver su info o para editarlo
    list_display_links = ['nombre', 'apellido']

    #sirve para poder agregar un filtrado en nuestro modelo
    #y esto servira para una busqueda mas rapida
    list_filter = ['nombre', 'apellido']

    #agrega un buscador y se coloca los atributos por los cuales buscara
    #no es sensible a mayuscula
    search_fields = ['nombre']



admin.site.register(Usuario, UsuarioAdmin)