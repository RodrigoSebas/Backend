from flask import Flask, request

from psycopg import connect

#esto es para crear un role admin que tenga contrasena porque por defecto no tienen contrasena
#create role admin with login superuser password 'rodrigo';
#tambien se puede eliminar drop role admin

conexion = connect(conninfo='postgresql://admin:rodrigo@localhost:5432/bd_flask')
#conexion = connect(conninfo='dbname=bd_flask user=rodrigo host=localhost port=5432 password=None')
# __name__ indicar si el arhivo que estamos utilizando es el archivo principal
app = Flask(__name__)

@app.route("/")
def manejar_ruta_inicio():
    return 'Bienvenido a mi api de flask'

@app.route("/registrar-usuario",methods=['POST'])
def manejar_registro_usuario():
    data = request.get_json()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO usuarios(nombre, apellido, correo) VALUES (%s,%s,%s)",(data['nombre'], data['apellido'],data['correo']))
    
    conexion.commit()
    cursor.close()
    return {
        'message':'usuario registrado exitosamente'
    }
@app.route("/listar-usuarios", methods=['GET'])
def devolver_usuarios():
    cursor = conexion.cursor()
    cursor.execute("select * from usuarios;")
    #cursor.fetchmany(10)
    #cursor.fetchone()
    usuarios = cursor.fetchall()
    users = []
    for user in usuarios:
        #print([{
         #   "id":user[0],
          #  "nombre":user[1],
           # "apellido":user[2],
            #"correo":user[3]
        #}])
        users.append({
            "id":user[0],
            "nombre":user[1],
            "apellido":user[2],
            "correo":user[3]
        })

    #print(usuarios)
    return {
        'content': users
    }






if __name__ == '__main__':
    app.run(debug=True)