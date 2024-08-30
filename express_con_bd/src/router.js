import { Router } from "express";
import { crearReceta,listarRecetas, actualizarReceta } from "./controllers/receta.controller.js";

export const enrutador = Router();

//cuando utilizamos el mismo endpoint para dos o mas controladores
// se recomienda agruparlos
//enrutador.post('/recetas', crearReceta);

enrutador.route("/recetas").post(crearReceta).get(listarRecetas)
enrutador.route("/receta/:id").put(actualizarReceta);
