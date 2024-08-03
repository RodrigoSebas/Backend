from flask_restful import Resource, request
from instancias import conexion
from models import CategoriaModel
from serializers import ManualCategoriaSerializer, CategoriaSerializer
from marshmallow.exceptions import ValidationError

class CategoriasController(Resource):
    def get(self):
        categorias = conexion.session.query(CategoriaModel).all()
        serializador = ManualCategoriaSerializer()
        respuesta = serializador.dump(categorias,many=True)
        return {
            'message':'Las categorias son:',
            'content':respuesta
        }
    
    def post(self):
        data = request.get_json()
        serializador = CategoriaSerializer()
        try:
            dataSerializada = serializador.load(data)
            nuevaCategoria = CategoriaModel(**dataSerializada)
            conexion.session.add(nuevaCategoria)
            conexion.session.commit()

            respuesta = serializador.dump(nuevaCategoria)
            return {
                'message':"categoria creada exitosamente",
                'content': respuesta
            },201
        except ValidationError as error:
            return {
                'message':'Error al crear la categoria',
                'content':error.args
            },400
        

class CategoriaController(Resource):
    def get(self, id):
        categoriaEncontrada = conexion.session.query(CategoriaModel).where(CategoriaModel.id==id).first()
        
        if not categoriaEncontrada:
            return{
                'message':'Categoria no existe'
            },404
        else:
            serializador = ManualCategoriaSerializer()
            resultado = serializador.dump(categoriaEncontrada)
            return {
                'content':resultado
            },200
