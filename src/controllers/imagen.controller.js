import AWS from "aws-sdk";
import { imagenSerializer } from "../serializers/imagen.serializer.js";
import { conexion } from "../instancias.js";

export const generarUrlFirmada = async (req, res) => {
  const { error, value } = imagenSerializer.validate(req.body);
  if (error) {
    return res.status(400).json({
      message: "Error al generar la imagen",
      content: error.details,
    });
  }

  const { key, path, contentType, extension } = value;
  const s3 = new AWS.S3();
  // getObject > obtener un archivo del s3
  //putObject > generar una url para subir un archivo al s3
  //deleteObject > eliminar un archivo del s3
  const url = s3.getSignedUrl("putObject", {
    Bucket: process.env.AWS_BUCKET_NAME,
    Key: `${path ? `${path}/` : ""}/${key}.${extension}`,
    Expires: 60,
    ContentType: contentType,
  });

  return res.json({
    content: url,
  });
};

export const crearImagen = async (req, res) => {
  const { error, value } = imagenSerializer.validate(req.body);

  if (error) {
    return res.status(400).json({
      message: "Error al crear la imagen",
      content: error.details,
    });
  }

  const imagenCreada = await conexion.imagen.create({
    data: { ...value },
  });

  return res.status(201).json({
    content: imagenCreada,
    message: "Imagen creada exitosamente",
  });
};

export const devolverImagen = async (req, res) => {
  const { id } = req.params;
  const imagenEncontrada = await conexion.imagen.findUniqueOrThrow({
    where: { id },
  });
  const s3 = new AWS.S3();

  s3.getSignedUrl("getObject", {
    Bucket: process.env.AWS_BUCKET_NAME,
    Key: imagenEncontrada.key,
    Expires: 100,
  })

  return res.json({
    content: url
  });
};
