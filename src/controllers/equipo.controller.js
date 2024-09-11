import { crearEquipoSerializer } from "../serializers/equipo.serializer.js"
import { conexion } from "../instancias.js"
    
export const crearEquipo = async (req, res) => {
    const {error, value} = crearEquipoSerializer.validate(req.body);

    if(error){
        return res.status(400).json({
            message: "Error al crear el equipo",
            content: error.details,
        });
    }
    

    const equipoCreado = await conexion.equipo.create({
        data: {
            nombre: value.nombre,
            imagen: value.imagen
        }
    })

    if(value.imagenId) {
        const imagenEncontrada = await conexion.imagen.findUniqueOrThrow({
            where: {id: value.imagenId},
            select: {id:true}
        })
        await conexion.imagen.update({
            where: {id: imagenEncontrada.id},
            data: {equipo: {connect: { id: equipoCreado.id}}}
        })
    }

    return res.status(201).json({
        message:"Equipo creado exitosamente",
        content: equipoCreado
    })
    
}

export const listarEquipos = async (req,res) => {
    const resultado = await conexion.equipo.findMany();

    return res.json({
        content:resultado,
    })
}