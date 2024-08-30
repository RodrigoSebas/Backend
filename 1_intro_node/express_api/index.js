import express from 'express'

const servidor = express()

//con esto se le dice al servidor que pueda enterder y convertir 
//la info del body de tipo application/json
servidor.use(express.json())

servidor.get('/', (req, res) => {
    res.status(201).json({
        message: 'Bienvenido a mi api de express'
    })
})

servidor.post('/registro', (req, res) => {
    //en express tenemos que indicarle que body va a poder recepcionar
    // si va a recepcionar json o xml o txt u otros
    console.log(req.body)
    res.json({
        message:'Registro completado exitosamente'
    })
})



servidor.listen(3000, () => {
    console.log("Servidor levantado exitosamente")
})