import express from "express";
import { config } from "dotenv";
import { enrutador } from "./router.js";

//a config se le puede agregar el path para indicarle el nombre
//del archivo con las variables de entorno en caso no se llama .env
config();

const servidor = express();

servidor.use(express.json());
const PUERTO = process.env.PORT;

const errorHandler = (error, req, res, next) => {
  console.log(error);
  let mensajePersonalizado;
  let status;
  switch(error.message){
    case "No Receta found":
        mensajePersonalizado = "La receta no existe";
        status = 404;
        break;
    
    case "No Preparacion found":
        mensajePersonalizado = "La preparacion no existe";
        status = 404
        break;

    case "No Ingrediente found":
        mensajePersonalizado = "El ingrediente no exite";
        status = 404
        break;

    default:
        mensajePersonalizado = error.message;
        status = 400
  }

  res.status(status).json({
    message: "Error al hacer la operacion",
    content: mensajePersonalizado,
  });
};


//agregando todas las rutas del enrutador al proyecto
servidor.use(enrutador);

servidor.use(errorHandler);

servidor.listen(PUERTO, () => {
  console.log(`Servidor inicado en el puerto ${PUERTO}`);
});
