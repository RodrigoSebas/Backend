from flask import Flask, request

# __name__ indicar si el arhivo que estamos utilizando es el archivo principal
app = Flask(__name__)

@app.route("/")
def manejar_ruta_inicio():
    return 'Bienvenido a mi api de flask'

@app.route("/registrar-usuario",methods=['POST'])
def manejar_registro_usuario():
    print(request.get_json())
    return {
        'message':'usuario registrado exitosamente'
    }




if __name__ == '__main__':
    app.run(debug=True)