import express from "express"
import morgan from "morgan"


const servidor = express()

//logger de los request del servidor
servidor.use(morgan("common"))

const PORT = process.env.PORT

servidor.listen(PORT, () => {
    console.log(`Servidor en pueto ${PORT}`)
})