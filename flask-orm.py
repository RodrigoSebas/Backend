from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, types

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:rodrigo@127.0.0.1:5432/colegio'
conexion = SQLAlchemy(app)

#pip install psycopg2-binary

class AlumnoModel(conexion.Model):
    id = Column(type_ = types.Integer, autoincrement=True, primary_key=True, nullable=False)
    nombre = Column(type_=types.Text, nullable=False)
    correo = Column(type_=types.Text, nullable=False, unique=True)
    fechaNacimiento = Column(name="fecha_nacimiento", type_=types.TIMESTAMP)

    #para inidicar el nombre de la tabla en la bd
    __tablename__="alumnos"



@app.route('/')
def inicio():
    conexion.create_all() #crea todos los modelos
    return {
        'message':'bienvenido a mi api'
    }

@app.route('/crear-alumno',methods=['POST'])
def crearAlumno():
    data = request.get_json()
    nuevoAlumno = AlumnoModel(nombre = data['nombre'],correo=data['correo'],fechaNacimiento=data['fechaNacimiento'])

    #agregarlo a la base de datos
    conexion.session.add(nuevoAlumno)

    #guardarlo de forma permanente
    conexion.session.commit()

    return {
        'message':"alumno registrado exitosamente"
    }, 201


if __name__ == '__main__':
    app.run(debug=True)