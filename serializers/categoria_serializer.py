from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import CategoriaModel
from marshmallow import Schema, fields

class CategoriaSerializer(SQLAlchemyAutoSchema):
    class Meta:
        model = CategoriaModel


class ManualCategoriaSerializer(Schema):
    id = fields.Integer(dump_only = True)
    nombre = fields.String(required=True)
    fechaCreacion = fields.DateTime(format="iso")
    disponibilidad = fields.Boolean()
