from models import UsuarioModel
from instancias import conexion
from flask_restful import Resource, request
from serializers import RegistroSerializer, LoginSerializer
from marshmallow.exceptions import ValidationError
from bcrypt import gensalt,hashpw, checkpw
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity


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
        identidad = get_jwt_identity()
        print(identidad)
        usuarioEncontrado = conexion.session.query(UsuarioModel).where(UsuarioModel.id==identidad).first()
        serializador = RegistroSerializer()
        resultado = serializador.dump(usuarioEncontrado)
        return {
            'content': resultado
        }