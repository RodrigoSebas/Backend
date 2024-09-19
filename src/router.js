import { Router } from "express";
import { crearEquipo, listarEquipos } from "./controllers/equipo.controller.js";
import asyncHandler from "express-async-handler";
import {
  registroUsuario,
  login,
  perfilUsuario,
} from "./controllers/usuario.controller.js";
import { validarToken, validarAdmin } from "./utils.js";
import {
  generarUrlFirmada,
  crearImagen,
  devolverImagen,
  devolverImagenEquipo
} from "./controllers/imagen.controller.js";

export const rutas = Router();

rutas
  .route("/equipos")
  .post(
    //asyncHandler(validarToken),
    //asyncHandler(validarAdmin),
    asyncHandler(crearEquipo)
  )
  .get(asyncHandler(listarEquipos));
rutas.route("/registro").post(asyncHandler(registroUsuario));
rutas.route("/login").post(asyncHandler(login));
//el orden es muy importante para la verificacion de la token
rutas
  .route("/perfil")
  .get(asyncHandler(validarToken), asyncHandler(perfilUsuario));

  
rutas.route("/generar-url").post(asyncHandler(generarUrlFirmada));

rutas.route("/imagen").post(asyncHandler(crearImagen));

rutas.route("/image/:id").get(asyncHandler(devolverImagen));

rutas.route("/imagen/equipo/:id").get(asyncHandler(devolverImagenEquipo))