import prisma, {USUARIO_ROL} from "@prisma/client";
import bcrypt from "bcrypt";

const conexion = new prisma.PrismaClient();

async function alimentarBD() {
  const usuarios = [
    {
      nombre: "Renzo Soles Contreras",
      email: "rsoles@gmail.com",
      password: bcrypt.hashSync("Welcome123!", 10),
      rol: USUARIO_ROL.ADMINISTRADOR,
    },
    {
      nombre: "Abel Guevara",
      email: "aguevara@gmail.com",
      password: bcrypt.hashSync("Welcome123!", 10),
      rol: USUARIO_ROL.CLIENTE,
    },
    {
      nombre: "Rodrigo Trujillo Mirano",
      email: "rtrujillo@gmail.com",
      password: bcrypt.hashSync("Welcome123!", 10),
      rol: USUARIO_ROL.ADMINISTRADOR,
    },
    {
      nombre: "Segundo Alvarez",
      email: "salvarez@gmail.com",
      password: bcrypt.hashSync("Welcome123!", 10),
      rol: USUARIO_ROL.CLIENTE,
    },
    {
      nombre: "Ignacio Estremadoyro",
      email: "iestremadoyry@gmail.com",
      password: bcrypt.hashSync("Welcome123!", 10),
      rol: USUARIO_ROL.CLIENTE,
    },
  ];

  //si tenemos un array de promesas y queremos que todas finalicen
  //entonces con promise all. si alguna falla, todas se quedan sin efecto
  await Promise.all(
    usuarios.map(async (usuario) => {
      //upsert > buscara el usuario en la bd y si encuentro lo actualiza y si no loc crea
      await conexion.usuario.upsert({
        create: {
          email: usuario.email,
          rol: usuario.rol,
          password: usuario.password,
        },
        update: {
          //para este caso no actualizamos nada
        },
        where: {
          email: usuario.email,
        },
      });
    })
  );
}

alimentarBD()
  .then(() => {
    console.log("Alimentacion a la bd finalizada exitosamente");
  })
  .catch(() => {
    console.log("Error al alimentar la bd");
  });
