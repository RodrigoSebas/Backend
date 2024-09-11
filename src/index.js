import express from "express"
import morgan from "morgan"
import {rutas} from "./router.js"
import AWS from "aws-sdk";
import cors from "cors"

const servidor = express()
servidor.use(cors({origin: "*"}))

AWS.config.update({
    region: process.env.AWS_BUCKET_REGION,
    credentials: {
      accessKeyId: process.env.AWS_ACCESS_KEY,
      secretAccessKey: process.env.AWS_SECRET_KEY,
    },
  });

const errorHandler = (error,req,res,next) => {
    res.status(400).json({
        message:"Error al iniciar la operacion",
        content: error.message
    })
};

//logger de los request del servidor
servidor.use(morgan("common"))

const PORT = process.env.PORT

servidor.use(express.json());
servidor.use(rutas)

servidor.use(errorHandler)

servidor.listen(PORT, () => {
    console.log(`Servidor en puerto ${PORT}`)
})