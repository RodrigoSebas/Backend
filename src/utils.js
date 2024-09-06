import jsonwebtoken from "jsonwebtoken";
import { conexion } from "./instancias.js";
import { USUARIO_ROL } from "@prisma/client";
//middleware manual
export const validarToken = async (req, res, next) => {
  const authorization = req.headers.authorization;

  if (!authorization) {
    return res.status(403).json({
      message: "Se necesita una token para realizar esta peticion",
    });
  }

  const token = authorization.split(" ")[1];

  if (!token) {
    return res.status(403).json({
      message: "Debe enviar la token formato 'Bearer TOKEN' ",
    });
  }

  try {
    const payload = jsonwebtoken.verify(token, process.env.JWT_SECRET);
    const usuarioEncontrado = await conexion.usuario.findUniqueOrThrow({
      where: { id: payload.usuarioId },
    });
    console.log(usuarioEncontrado);
    //se crea el usuario en el request para guardar el usuarioencontrado y poder verlo despues en el controlador final
    req.usuario = usuarioEncontrado;
    next();
  } catch (error) {
    return res.status(403).json({
      message: "Error al verificar la token",
      content: error.message,
    });
  }
};

export const validarAdmin = async (req, res, next) => {
  const { rol } = req.usuario;

  if (rol === USUARIO_ROL.ADMINISTRADOR) {
    next();
  } else {
    return res.status(403).json({
      message: "Usuario con permisos insuficientes",
    });
  }
};

export const validarCliente = async (req, res, next) => {
    const { rol } = req.usuario;
  
    if (rol === USUARIO_ROL.CLIENTE) {
      next();
    } else {
      return res.status(403).json({
        message: "Usuario con permisos insuficientes",
      });
    }
  };
  