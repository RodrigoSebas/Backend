from models import UsuarioModel
from instancias import conexion
from flask_restful import Resource, request
from serializers import RegistroSerializer, LoginSerializer, ActualizarUsuarioSerializer, CambiarPasswordSerializer, ResetearPasswordSerializer, ConfirmarResetTokenSerializer, ConfirmarResetPasswordSerializer
from marshmallow.exceptions import ValidationError
from bcrypt import gensalt,hashpw, checkpw
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from utilitarios import enviarCorreo, encriptarTexto, desencriptarTexto
from json import loads, dumps

class RegistroController(Resource):
    def post(self):
        data = request.get_json()
        serializer = RegistroSerializer()
        try:
            dataValidada = serializer.load(data)
            print(dataValidada)

            salt = gensalt()
            password = dataValidada.get("password")
            passwordBytes = bytes(password,'utf-8')
            hash = hashpw(passwordBytes,salt)
            hashString = hash.decode('utf-8')

            dataValidada['password'] = hashString
            nuevoUsuario = UsuarioModel(**dataValidada)
            conexion.session.add(nuevoUsuario)
            conexion.session.commit()
            resultado = serializer.dump(nuevoUsuario)

            return {
                'message':'Usuario creado exitosamente',
                'content':resultado
                
            },201
        except ValidationError as error:
            return {
                'message':'Error al crear el usuario',
                'content':error.args
            },400
        
        except IntegrityError as error:
            return {
                'message':'Error al crear el usuario',
                'content':'El usuario con correo {} ya existe'.format(data.get("correo"))
            },400


class LoginController(Resource):
    def post(self):
        data = request.get_json()
        serializador = LoginSerializer()
        try:
            dataSerializada = serializador.load(data)
            usuario = conexion.session.query(UsuarioModel).where(UsuarioModel.correo==dataSerializada.get('correo')).first()

            if not usuario:
                return {
                    'message':'usuario no existe'
                },404
            
            password = usuario.password
            passwordBytes = bytes(password,'utf-8')
            passwordEntranteBytes = bytes(dataSerializada.get("password"),'utf-8')
            validacionPassword = checkpw(passwordEntranteBytes,passwordBytes)

            if validacionPassword == False:
                return {
                    'message':'Credenciales incorrectas'
                },400
            informacionAdicional = {
                'correo':usuario.correo
            }
            jwt = create_access_token(identity=usuario.id, additional_claims=informacionAdicional)
            
            return {
                    'message':"Bienvenido",
                    'content':jwt
                }

        except ValidationError as error:
            return {
                'message':'Error al hacer el login',
                'content':error.args
            }
        
class PerfilController(Resource):
    @jwt_required()
    def get(self):
        #devuelve el id del usuario o identificador de la token
        identidad = get_jwt_identity() #obtiene el id del usuario actual

        print(identidad)
        usuarioEncontrado = conexion.session.query(UsuarioModel).where(UsuarioModel.id==identidad).first()
        serializador = RegistroSerializer()
        resultado = serializador.dump(usuarioEncontrado)
        return {
            'content': resultado
        }
    
    @jwt_required()
    def put(self):
        identificador = get_jwt_identity()

        usuarioEncontrado = conexion.session.query(UsuarioModel).where(UsuarioModel.id==identificador).first()
        data = request.get_json()

        if not usuarioEncontrado:
            return {
                'message':'El usuario no se encuentra en la base de datos'
            },400

        try:
            serializador = ActualizarUsuarioSerializer()
            dataValidada = serializador.load(data)

            usuarioEncontrado.nombre = dataValidada.get("nombre")
            conexion.session.commit()
            
            #esto es solo para tener todos los datos y no solo el nombre que seria con actualizarUsuarioSerializer
            serializadorUsuario = RegistroSerializer()
            resultado = serializadorUsuario.dump(usuarioEncontrado)

            return {
                'message': 'Usuario actualizado exitosamente',
                'content':resultado
            }

        except ValidationError as error:
            return {
                'message':'Error al actualizar el usuario',
                'content':error.args
            },400
        

class CambiarPasswordController(Resource):
    @jwt_required()
    def put(self):
        data = request.get_json()
        identificador = get_jwt_identity()
        serializador = CambiarPasswordSerializer()
        try:
            dataValidada = serializador.load(data)
            usuarioEncontrado = conexion.session.query(UsuarioModel).where(UsuarioModel.id == identificador).first()

            if not usuarioEncontrado:
                return {
                    'message':"Usuario no existe"
                },404
            
            passwordAntigua = dataValidada.get('passwordAntigua')
            passwordAntiguaBytes = bytes(passwordAntigua,'utf-8')
            passwordActual = usuarioEncontrado.password
            passwordActualBytes = bytes(passwordActual,'utf-8')
            validacionPassword = checkpw(passwordAntiguaBytes,passwordActualBytes)

            if validacionPassword == False:
                return {
                    'message':"Password antigua invalida"
                },400
            
            salt = gensalt()
            passwordNueva = dataValidada.get("passwordNueva")
            passwordNuevaBytes = bytes(passwordNueva,'utf-8')
            hash = hashpw(passwordNuevaBytes,salt)
            hashString = hash.decode('utf-8')
            
            usuarioEncontrado.password = hashString

            conexion.session.commit()

            return {
                'message':"Password actualizada exitosamente"
            }
            
        except ValidationError as error:
            return {
                'message':'Error al cambiar la password',
                'content':error.args
            },400


class ResetearPasswordController(Resource):
    def post(self):
        data = request.get_json()
        serializer = ResetearPasswordSerializer()

        try:
            dataSerializada = serializer.load(data)
            usuarioEncontrado = conexion.session.query(UsuarioModel).where(UsuarioModel.correo==dataSerializada.get("correo")).first()
            
            if not usuarioEncontrado:
                return {
                    'message':'El usuario no existe en la base de datos'
                },400
            
            textoAEncriptar = {
                'correo':usuarioEncontrado.correo
            }
            #dumps en el modulo json lo que hace es convierte un diccionario a un string
            token = encriptarTexto(dumps(textoAEncriptar))
            url = f'http://localhost:5000/reset-password-frontend?token={token}'
            
            textocorreo = """
Hola {},
Has solicitado el cambio de la password de tu cuenta en Tienditapp, haz click en el siguiente <a href="{}">link<a> para proceder
<br>

<br>
si no has sido tu omite este mensaje.
<br>
<br>

Gracias,
<br>
Atentamente.

El equipo mas chevere de todos""".format(usuarioEncontrado.nombre,url)

            htmlCorreo = """
<html>
<body>
<p>Hola <b>{}</b>, <br>
Has solicitado el cambio de la password de tu cuenta en Tienditapp, si no has sido tu omite este mensaje.

Gracias,

Atentamente.

El equipo mas chevere de todos
</p>
</body>
</html>
"""
            
           
            plantillaCorreo = open('plantilla_mensajeria.html','r')
            textoPlantilla = plantillaCorreo.read()
            textoResultado = textoPlantilla.replace('cuerpo_correo',textocorreo)

            enviarCorreo(usuarioEncontrado.correo,'Has solicitado el cambio de password',textocorreo,textoResultado)

            return {
                'message':'Reset completado exitosamente'
            }
        except ValidationError as error:
            return {
                'message':'Error al resetear la password',
                'content':error.args
            },400


class ConfirmarResetTokenController(Resource):
    def post(self):
        data = request.get_json()
        serializador = ConfirmarResetTokenSerializer()
        try:
            dataValidada = serializador.load(data)
            #loads convierte un string en diccionario
            informacion = loads(desencriptarTexto(dataValidada.get('token')))
            usuarioEncontrado = conexion.session.query(UsuarioModel).where(UsuarioModel.correo == informacion.get("correo")).first()
            if not usuarioEncontrado:
                return {
                    'message':'Usuario no existe'
                },400

            serializer = RegistroSerializer()
            resultado = serializer.dump(usuarioEncontrado)
            return{
                'content':resultado
            }
        except ValidationError as error:
            return {
                'message':'Error al hacer el request',
                'content': error.args
            },400
        

class ConfirmarResetPasswordController(Resource):
    def post(self):
        data = request.get_json()
        serializador = ConfirmarResetPasswordSerializer()

        try:
            dataValidada = serializador.load(data)
            informacion = loads(desencriptarTexto(dataValidada.get('token')))
            
            usuarioEncontrado = conexion.session.query(UsuarioModel).where(UsuarioModel.correo == informacion.get("correo")).first()
            if not usuarioEncontrado:
                return {
                    'message':'Usuario no existe'
                },400
            
            salt = gensalt()
            passwordNueva = dataValidada.get("nuevaPassword")
            passwordNuevaBytes = bytes(passwordNueva,'utf-8')
            hash = hashpw(passwordNuevaBytes,salt)
            hashString = hash.decode('utf-8')
            
            usuarioEncontrado.password = hashString

            conexion.session.commit()

            return {
                'message':'Password modificada exitosamente'
            },200
            

        except ValidationError as error:
            return {
                'message':'Error al cambiar la password',
                'content':error.args
            },400
