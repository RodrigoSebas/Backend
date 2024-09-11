/*
  Warnings:

  - You are about to drop the `Imagen` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE "Imagen" DROP CONSTRAINT "Imagen_equipo_id_fkey";

-- DropForeignKey
ALTER TABLE "Imagen" DROP CONSTRAINT "Imagen_jugador_id_fkey";

-- DropTable
DROP TABLE "Imagen";

-- CreateTable
CREATE TABLE "imagenes" (
    "id" UUID NOT NULL,
    "key" TEXT NOT NULL,
    "path" TEXT,
    "content_type" TEXT NOT NULL,
    "extension" TEXT NOT NULL,
    "equipo_id" UUID,
    "jugador_id" UUID,

    CONSTRAINT "imagenes_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "imagenes_key_key" ON "imagenes"("key");

-- AddForeignKey
ALTER TABLE "imagenes" ADD CONSTRAINT "imagenes_equipo_id_fkey" FOREIGN KEY ("equipo_id") REFERENCES "equipos"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "imagenes" ADD CONSTRAINT "imagenes_jugador_id_fkey" FOREIGN KEY ("jugador_id") REFERENCES "jugadores"("id") ON DELETE SET NULL ON UPDATE CASCADE;
