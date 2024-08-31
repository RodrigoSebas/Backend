import { prisma } from "../cliente.js";
import { PreparacionSerializer } from "../serializers/preparacion.serializer.js";

export const crearPreparacion = async (req, res) => {
  const { error, value } = PreparacionSerializer.validate(req.body);
  if (error) {
    return res.status(400).json({
      message: "Error al crear la preparacion",
      content: error.details,
    });
  }

  const preparacionExistente = await prisma.preparacion.findFirst({
    where: {recetaId :value.recetaId},
    orderBy: {orden: "desc"},
    select: {orden: true}
  })

  //let nuevaPosicion;
  //if(preparacionExistente){
    //nuevaPosicion = preparacionExistente.orden +1
  //} else{
    //nuevaPosicion = 1;
  //}

  const nuevaPosicion = preparacionExistente ? preparacionExistente.orden+1 : 1;

  const nuevaPreparacion = await prisma.preparacion.create({
    data: {
        descripcion: value.descripcion,
        recetaId: value.recetaId,
        orden: nuevaPosicion
    }
  })

  return res.status(201).json({
    message: "Preparacion creada exitosamente",
    content: nuevaPreparacion,
  })
};
