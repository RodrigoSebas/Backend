from django.db import models

# Create your models here.

class Categoria(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False)
    nombre = models.TextField(null=False)
    habilitado = models.BooleanField(default=True, null=False)

    class Meta:
        db_table = 'categorias' #nombre de la tabla
        ordering = ['nombre'] # -nombre es en orden descendente, nombre para ascendente


class Golosina(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False)
    nombre = models.TextField(null=False)
    precio = models.FloatField()
    imagen = models.ImageField(upload_to='/imagenes', null=True)
    habilitado = models.BooleanField(default=True)
    
    # on_delete > que va a suceder con los registros que tengan relacion con la categoria eliminada
    # CASCADE > elimina la categoria y elimina las golosinas
    # PROTECT > evita la eliminacion de la categoria y lanza un error de tipo ProtectError
    # RESTRICT > similar al PROTECT pero lanzara un error de tipo RestrictedError
    # SET_NULL > elimina la categoria y cambia el valor de la columna categoria_id de sus golosinas a null
    # SET_DEFAULT > elimina la categoria y cambia el valor a un valor por defecto
    # DO_NOTHING > JAMAS USAR ESTO! elimina la categoria y deja como esta el valor de la columna generando incongruencia de datos 
    
    categoria = models.ForeignKey(to=Categoria, db_column='categoria_id', on_delete=models.PROTECT)

    class Meta:
        db_table = 'golosinas'
        ordering = ['nombre', 'precio']
        #unique_together sirve para crear unicidad entre dos o mas columnas
        unique_together = [['nombre','precio']]