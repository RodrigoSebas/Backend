import { USUARIO_ROL } from "@prisma/client";
import Joi from "joi";

export const registroUsuarioSerializer = Joi.object({
  email: Joi.required().email(),
  password: Joi.required().regex(),
  rol: Joi.string()
    .required()
    .allow(USUARIO_ROL.ADMINISTRADOR, USUARIO_ROL.CLIENTE),
});
