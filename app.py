from flask import Flask
from instancias import conexion
from dotenv import load_dotenv
from os import environ
from models import *
from flask_migrate import Migrate
from controllers import *
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta

#variables de entorno
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URL")
app.config['JWT_SECRET_KEY'] = environ.get("JWT_SECRET")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1,minutes=10,seconds=5)

JWTManager(app)

#definimos la api de nuestra aplicacion de flask
api = Api(app)


conexion.init_app(app)

Migrate(app, conexion)

#agregamos los recursos (controladores)
api.add_resource(CategoriasController, '/categorias')
api.add_resource(CategoriaController, '/categoria/<int:id>')
api.add_resource(ProductosController, '/productos')
api.add_resource(RegistroController, '/registro')
api.add_resource(LoginController,'/login')
api.add_resource(PerfilController, '/perfil')
if __name__=="__main__":
    app.run(debug=True)





