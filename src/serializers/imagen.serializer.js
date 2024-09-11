import Joi from "joi";

export const imagenSerializer = Joi.object({
  key: Joi.string().required(),
  path: Joi.string().optional(),
  contentType: Joi.string()
    .required()
    .allow("image/jpg", "image/png", "image/jpeg","image/svg+xml","application/pdf"),
  extension: Joi.string().required().allow("png", "jpg", "jpeg", "svg","pdf"),
});
