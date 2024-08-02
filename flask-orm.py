from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, types
from flask_migrate import Migrate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.exceptions import ValidationError
from sqlalchemy.sql.expression import and_
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:rodrigo@127.0.0.1:5432/colegio'
conexion = SQLAlchemy(app)
Migrate(app,conexion)
#flask --app flask-orm:app db init (esto es porque el archivo no se llama app sirve para inicializar)
#flask --app flask-orm:app db migrate -m "mensaje"
#flask --app flask-orm:app db upgrade


#pip install psycopg2-binary

class AlumnoModel(conexion.Model):
    id = Column(type_ = types.Integer, autoincrement=True, primary_key=True, nullable=False)
    nombre = Column(type_=types.Text, nullable=False)
    correo = Column(type_=types.Text, nullable=False, unique=True)
    fechaNacimiento = Column(name="fecha_nacimiento", type_=types.TIMESTAMP)

    #para inidicar el nombre de la tabla en la bd
    __tablename__="alumnos"

class AlumnoSerializer(SQLAlchemyAutoSchema):
    class Meta:
        model = AlumnoModel



@app.route('/')
def inicio():
    conexion.create_all() #crea todos los modelos
    return {
        'message':'bienvenido a mi api'
    }

@app.route('/crear-alumno',methods=['POST'])
def crearAlumno():
    data = request.get_json()
    serializador = AlumnoSerializer()
    dataValidada = serializador.load(data)
    
    print(dataValidada)
    nuevoAlumno = AlumnoModel(nombre = data['nombre'],correo=data['correo'],fechaNacimiento=data['fechaNacimiento'])

    #agregarlo a la base de datos
    conexion.session.add(nuevoAlumno)

    #guardarlo de forma permanente
    conexion.session.commit()

    return {
        'message':"alumno registrado exitosamente"
    }, 201

@app.route("/listar-alumnos", methods=['GET'])
def listarAlumnos():
    alumnos = conexion.session.query(AlumnoModel).all()
    print(alumnos)

    serializador = AlumnoSerializer()
    resultado = serializador.dump(alumnos,many=True)
    return {
        'content':resultado
    }


@app.route("/devolver-alumno/<int:id>",methods=['GET'])
def devolverAlumno(id):
    alumno = conexion.session.query(AlumnoModel).where(AlumnoModel.id==id).first()

    if not alumno:
        return {
            "message":"alumno no encontrado"
        },404
    
    serializador = AlumnoSerializer()
    resultado = serializador.dump(alumno)
    return {
        'content': resultado
    }
    
@app.route("/actualizar-alumno/<int:id>",methods=['PUT'])
def actualizarAlumno(id):
    alumno = conexion.session.query(AlumnoModel).with_entities(AlumnoModel.id).where(AlumnoModel.id==id).first()

    if not alumno:
        return {
            "message":"alumno no encontrado"
        },404

    serializador = AlumnoSerializer()
    try:
        dataValidada = serializador.load(request.get_json())
        resultado = conexion.session.query(AlumnoModel).where(AlumnoModel.id==id).update(dataValidada)
        conexion.session.commit()
        print(resultado)

        resultado = conexion.session.query(AlumnoModel).where(AlumnoModel.id==id).first()
        alumnoActualizado = serializador.dump(resultado)
        return {
            "message":"alumno actualizado correctamente",
            "content":alumnoActualizado
        }
    except ValidationError as error:
        return {
            'message': 'error al actualizar el alumno',
            'content': error.args
        },400
    
@app.route("/eliminar-alumno/<int:id>",methods=['DELETE'])
def eliminarAlumno(id):
    alumno = conexion.session.query(AlumnoModel).with_entities(AlumnoModel.id).where(AlumnoModel.id==id).first()

    if not alumno:
        return {
            "message":"alumno no encontrado"
        },404
    conexion.session.query(AlumnoModel).where(AlumnoModel.id==id).delete()
    conexion.session.commit()

    return {
        "message":"alumno eliminado correctamente"
    }

@app.route("/buscar-alumnos",methods=['GET'])
def buscarAlumnos():
    queryParams = request.args
    nombre = queryParams.get("nombre")
    correo = queryParams.get("correo")
    condiciones = []
    if nombre:
        #condiciones.append(AlumnoModel.nombre==nombre) #busqueda exacta
        #condiciones.append(AlumnoModel.nombre.like(f"%{nombre}%")) #busqueda por similitud respetando mayusculas
        condiciones.append(AlumnoModel.nombre.ilike(f"%{nombre}%")) #busqueda por similitud sin respetar mayusculas


        
    if correo:
        #condiciones.append(AlumnoModel.correo==correo)
        condiciones.append(AlumnoModel.correo.ilike(f"%{correo}%"))

    resultado = conexion.session.query(AlumnoModel).where(and_(*condiciones)).all()
    serializer = AlumnoSerializer()
    alumnos = serializer.dump(resultado,many=True)
    print(resultado)
    return {
        "message":alumnos
    }

# TODO EN ORM
# Crear una tabla llamada productos cuya clase sea ProductoModel
# id AI pk not null
# nombre texto not null
# precio float 
# disponible boolean

# ingresar los siguientes valores
class ProductoModel(conexion.Model):
    id = Column(type_ = types.Integer, autoincrement=True, primary_key=True, nullable=False)
    nombre = Column(type_=types.Text, nullable=False)
    precio = Column(type_=types.Float)
    disponible = Column(type_=types.Boolean)

    #para inidicar el nombre de la tabla en la bd
    __tablename__="productos"

class ProductoSerializer(SQLAlchemyAutoSchema):
    class Meta:
        model = ProductoModel

# hacer una busqueda de los productos por su nombre (usando el ilike)
@app.route("/buscar-producto-por-nombre",methods=['GET'])
def buscarProductoPorNombre():
    queryParams = request.args
    nombre = queryParams.get("nombre")
    disponible = queryParams.get("disponible")
    condiciones=[]
    if nombre:
        #condiciones.append(AlumnoModel.nombre==nombre) #busqueda exacta
        #condiciones.append(AlumnoModel.nombre.like(f"%{nombre}%")) #busqueda por similitud respetando mayusculas
        condiciones.append(ProductoModel.nombre.ilike(f"%{nombre}%")) #busqueda por similitud sin respetar mayusculas
        #condiciones.append(ProductoModel.disponible==True)
    
    resultado = conexion.session.query(ProductoModel).where(and_(*condiciones)).all()
    serializer = ProductoSerializer()
    productos = serializer.dump(resultado,many=True)
    print(productos)
    return {
        "message":productos
    }

# hacer otra busqueda de los productos en un rango de precio (precio minimo y precio maximo)


# Quiero los productos que cuesten entre 5 y 15 soles

# en ambas busquedas solamente buscar los productos que esten disponibles

if __name__ == '__main__':
    app.run(debug=True)