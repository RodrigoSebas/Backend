import express from "express"
import morgan from "morgan"
import {rutas} from "./router.js"

const servidor = express()
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