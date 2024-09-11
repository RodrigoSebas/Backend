/*
  Warnings:

  - You are about to drop the `Partido` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE "Partido" DROP CONSTRAINT "Partido_equipo_local_id_fkey";

-- DropForeignKey
ALTER TABLE "Partido" DROP CONSTRAINT "Partido_equipo_visitante_id_fkey";

-- DropForeignKey
ALTER TABLE "Partido" DROP CONSTRAINT "Partido_fecha_id_fkey";

-- DropTable
DROP TABLE "Partido";

-- CreateTable
CREATE TABLE "partidos" (
    "id" UUID NOT NULL,
    "fecha_id" UUID NOT NULL,
    "equipo_local_id" UUID NOT NULL,
    "equipo_visitante_id" UUID NOT NULL,
    "fecha_partido" DATE NOT NULL,
    "hora" TIME NOT NULL,
    "zona_horaria" TEXT NOT NULL,
    "lugar" TEXT NOT NULL,
    "estado" "PARTIDO_ESTADO" NOT NULL DEFAULT 'POR_EMPEZAR',
    "marcador_local" INTEGER NOT NULL,
    "marcador_visitante" INTEGER NOT NULL,

    CONSTRAINT "partidos_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "partidos" ADD CONSTRAINT "partidos_fecha_id_fkey" FOREIGN KEY ("fecha_id") REFERENCES "fechas"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "partidos" ADD CONSTRAINT "partidos_equipo_local_id_fkey" FOREIGN KEY ("equipo_local_id") REFERENCES "equipos"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "partidos" ADD CONSTRAINT "partidos_equipo_visitante_id_fkey" FOREIGN KEY ("equipo_visitante_id") REFERENCES "equipos"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
