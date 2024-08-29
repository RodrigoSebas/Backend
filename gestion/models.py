from django.db import models
#si queremos usar las columnas de la tabla authuser y agregar otras columnas se usa
#ABtractbuser  caso contrario usamos abstractbaseuser
from django.contrib.auth.models import (AbstractBaseUser, 
                                        BaseUserManager,
                                        PermissionsMixin)
from uuid import uuid4
from cloudinary.models import CloudinaryField
# Create your models here.

class UsuarioManager(BaseUserManager):
    def create_superuser(self, correo, nombre, apellido, password):
        if not correo:
            raise ValueError('el usuario debe tener un correo')
        if not nombre:
            raise ValueError('el usuario debe tener un nombre')
        if not apellido:
            raise ValueError('el usuario debe tener un apellido')
        #quita los espacios al comienzo y al final y pone todo en minusculas
        correo_normalizado = self.normalize_email(correo)
        nuevo_usuario = self.model(correo=correo_normalizado, nombre = nombre, apellido = apellido)
        nuevo_usuario.set_password(password)

        nuevo_usuario.is_superuser = True
        nuevo_usuario.is_staff = True

        nuevo_usuario.save()

class Usuario(AbstractBaseUser, PermissionsMixin):
    #DOS VECES PORQUE EL PRIMERO SE USAR PARA GUARDAR EN LA BASE DE DATOS
    #MIENTRAS LA SEGUNDA SERA PARA COMO SE MOSTRARA AL RETORNAR LA INFO DE LA BASE DE DATOS
    opcionesTipoUsuario = [['NOVIO', 'NOVIO'], 
                           ['INVITADO','INVITADO'], 
                           ['ADMIN','ADMIN']]
    id = models.AutoField(primary_key=True)
    nombre = models.TextField(null = False)
    apellido = models.TextField(null = False)
    correo = models.EmailField(null = False, unique=True)
    numeroTelefonico = models.TextField(db_column='numero_telefonico')
    password = models.TextField(null=False)
    tipoUsuario = models.TextField(choices=opcionesTipoUsuario, db_column='tipo_usuario')

    #opcionalmente agregaremos las columnas para que funcione el panel
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    #como se va comportar al momento de crear el usaurio por la terminal
    objects = UsuarioManager()

    class Meta:
        db_table = 'usuarios'



class ListaNovio(models.Model):
    id = models.AutoField(primary_key=True)
    novio = models.ForeignKey(to=Usuario, on_delete=models.RESTRICT, db_column='novio_id', null=False, related_name='usuario_novio')
    novia = models.ForeignKey(to=Usuario, on_delete=models.RESTRICT, db_column='novia_id', null=False, related_name='usuario_novia')

    codigo = models.UUIDField(default=uuid4)

    class Meta:
        db_table = 'lista_novios'

class Regalo(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.TextField(null=False)
    descripcion = models.TextField()
    precio = models.FloatField()
    url = models.URLField()
    imagen = CloudinaryField('imagen')
    ubicacion = models.TextField()
    cantidad = models.IntegerField(null=False)
    habilitado = models.BooleanField(default=True)
    ListaNovio = models.ForeignKey(to=ListaNovio, on_delete=models.RESTRICT, db_column='lista_novios_id')


class Reservacion(models.Model):
    id = models.AutoField(primary_key=True)
    cantidad = models.IntegerField(null=False)
    regalo = models.ForeignKey(to=Regalo, on_delete=models.RESTRICT, db_column='regalo_id', null=False)
    usuario = models.ForeignKey(to=Usuario, on_delete=models.RESTRICT, db_column='usuario_id', null=False)
    createdAt = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updateAt = models.DateTimeField(auto_now=True, db_column='updated_at')
    class Meta:
        db_table = 'reservaciones'