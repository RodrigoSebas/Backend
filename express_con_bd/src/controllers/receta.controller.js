import { prisma } from "../cliente.js";
import { RecetaSerializer } from "../serializers/receta.serializer.js";

export async function crearReceta(req, res) {
  const body = req.body;
  const resultado = await prisma.receta.create({
    data: {
      nombre: body.nombre,
      descripcion: body.descripcion,
    },
  });

  return res.json({
    message: "Receta creada exitosamente",
    content: resultado,
  });
}

export const listarRecetas = async (req, res) => {
  const resultado = await prisma.receta.findMany();
  return res.json({
    content: resultado,
  });
};

export const actualizarReceta = async (req, res) => {
  const body = req.body;
  const id = req.params.id;
  //const {id} = req.params; //otra forma

  const { error, value } = RecetaSerializer.validate(body);

  if (error) {
    return res.status(400).json({
      message: "Error al actualizar la receta",
      content: error.details,
    });
  }

  // obtiene todos los campos de la receta, vamos a especificar que solo queremos el idw
  const recetaEncontrada = await prisma.receta.findUniqueOrThrow({
    where: { id: +id },
    select: { id: true },
  });

  const recetaActualizada = await prisma.receta.update({
    where: { id: recetaEncontrada.id },
    data: {
      nombre: value.nombre,
      descripcion: value.descripcion,
      habilitado: value.habilitado,
    },
  });

  return res.json({
    message: "Receta actualizada correctamente",
    content: recetaActualizada,
  });
};

export const eliminarReceta = async (req, res) => {
  const { id } = req.params;

  const recetaEncontrada = await prisma.receta.findUniqueOrThrow({
    where: { id: +id },
    select: { id: true },
  });

  const resultado = await prisma.receta.delete({
    where: { id: recetaEncontrada.id },
  });

  return res.json({
    message: "receta eliminada exitosamente",
    content: resultado,
  });
};

export const listarRecetaPorId = async (req, res) => {
  const { id } = req.params;

  const recetaEncontrada = await prisma.receta.findFirstOrThrow({
    where: { id: +id },
    //incluir modelos anidados
    include: {
      ingredientes: true,
      preparaciones: {
        orderBy: {orden: "desc"}
      }
    }
  });

  return res.json({
    content: recetaEncontrada,
  });
};
