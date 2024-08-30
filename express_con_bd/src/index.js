import express from 'express'
import {config} from 'dotenv'
import { enrutador } from './router.js' 

//a config se le puede agregar el path para indicarle el nombre 
//del archivo con las variables de entorno en caso no se llama .env
config()

const servidor = express()


servidor.use(express.json())
const PUERTO = process.env.PORT

//agregando todas las rutas del enrutador al proyecto
servidor.use(enrutador)


servidor.listen(PUERTO, () => {
    console.log(`Servidor inicado en el puerto ${PUERTO}`)
})