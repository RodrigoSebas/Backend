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