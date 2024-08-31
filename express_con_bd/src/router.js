import { Router } from "express";
import {
  crearReceta,
  listarRecetas,
  actualizarReceta,
  eliminarReceta,
  listarRecetaPorId
} from "./controllers/receta.controller.js";

import { crearIngrediente } from "./controllers/ingrediente.controller.js";
import { crearPreparacion } from "./controllers/preparacion.controller.js"

import asyncHandler from "express-async-handler";
export const enrutador = Router();

//cuando utilizamos el mismo endpoint para dos o mas controladores
// se recomienda agruparlos
//enrutador.post('/recetas', crearReceta);

enrutador
  .route("/recetas")
  .post(asyncHandler(crearReceta))
  .get(asyncHandler(listarRecetas));
enrutador
  .route("/receta/:id")
  .put(asyncHandler(actualizarReceta))
  .delete(asyncHandler(eliminarReceta))
  .get(asyncHandler(listarRecetaPorId));

enrutador.route("/ingredientes").post(asyncHandler(crearIngrediente));

enrutador.route("/preparaciones").post(asyncHandler(crearPreparacion));


