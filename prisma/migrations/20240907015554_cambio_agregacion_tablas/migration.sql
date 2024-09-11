/*
  Warnings:

  - You are about to drop the column `imagen` on the `equipos` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "equipos" DROP COLUMN "imagen";

-- CreateTable
CREATE TABLE "Imagen" (
    "id" UUID NOT NULL,
    "key" TEXT NOT NULL,
    "path" TEXT,
    "content_type" TEXT NOT NULL,
    "extension" TEXT NOT NULL,
    "equipo_id" UUID,
    "jugador_id" UUID,

    CONSTRAINT "Imagen_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Imagen_key_key" ON "Imagen"("key");

-- AddForeignKey
ALTER TABLE "Imagen" ADD CONSTRAINT "Imagen_equipo_id_fkey" FOREIGN KEY ("equipo_id") REFERENCES "equipos"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Imagen" ADD CONSTRAINT "Imagen_jugador_id_fkey" FOREIGN KEY ("jugador_id") REFERENCES "jugadores"("id") ON DELETE SET NULL ON UPDATE CASCADE;
