from flask import Flask
from instancias import conexion
from dotenv import load_dotenv
from os import environ
from models import *
from flask_migrate import Migrate
from controllers import *
from flask_restful import Api

#variables de entorno
load_dotenv()

app = Flask(__name__)


#definimos la api de nuestra aplicacion de flask
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URL")

conexion.init_app(app)

Migrate(app, conexion)

#agregamos los recursos (controladores)
api.add_resource(CategoriasController, '/categorias')
api.add_resource(CategoriaController, '/categoria/<int:id>')
api.add_resource(ProductosController, '/productos')

if __name__=="__main__":
    app.run(debug=True)





