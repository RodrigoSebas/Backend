import express from "express";

const servidor = express();

servidor.listen(process.env.PORT, () => {
  console.log(`servidor corriendo en el puerto ${PORT}`);
});
