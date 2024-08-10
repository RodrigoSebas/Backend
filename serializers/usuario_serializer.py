from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import validate #funciones que ayudaran con validaciones adicionales
from models import UsuarioModel, TipoUsuario
from marshmallow_enum import EnumField
from marshmallow import Schema, fields

class RegistroSerializer(SQLAlchemyAutoSchema):
    #ademas de las validaciones que nos brinda marsmallow le estamos agregando validar un correo
    tipoUsuario = EnumField(TipoUsuario)
    correo = auto_field(validate=validate.Email(error='El correo no cumple con el formato correcto'))
    password = auto_field(load_only=True)
    class Meta:
        model = UsuarioModel

class LoginSerializer(Schema):
    correo = fields.Email(required=True)
    password = fields.String(required=True)

class ActualizarUsuarioSerializer(Schema):
    nombre = fields.String(required=True)

class CambiarPasswordSerializer(Schema):
    passwordAntigua = fields.String(required=True)
    #expresion regular para tener una password segura
    passwordNueva = fields.String(required=True, validate=validate.Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&?!])[A-Za-z\d@#$%^&?!]{6,}$"))

class ResetearPasswordSerializer(Schema):
    correo = fields.Email(required=True)
    
class ConfirmarResetTokenSerializer(Schema):
    token = fields.String(required=True)

class ConfirmarResetPasswordSerializer(Schema):
    token = fields.String(required=True)
    nuevaPassword = fields.String(required=True, validate=validate.Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&?!])[A-Za-z\d@#$%^&?!]{6,}$"))
