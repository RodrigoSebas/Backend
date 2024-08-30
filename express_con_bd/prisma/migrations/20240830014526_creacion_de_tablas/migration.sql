-- CreateTable
CREATE TABLE "recetas" (
    "id" SERIAL NOT NULL,
    "nombre" TEXT NOT NULL,
    "descripcion" TEXT,
    "habilitado" BOOLEAN NOT NULL DEFAULT true,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "recetas_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Ingredientes" (
    "id" SERIAL NOT NULL,
    "titulo" TEXT NOT NULL,
    "receta_id" INTEGER NOT NULL,

    CONSTRAINT "Ingredientes_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "preparaciones" (
    "id" SERIAL NOT NULL,
    "orden" INTEGER NOT NULL,
    "descripcion" TEXT NOT NULL,
    "updatedAt" TIMESTAMP(3) NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "receta_id" INTEGER NOT NULL,

    CONSTRAINT "preparaciones_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "preparaciones_orden_receta_id_key" ON "preparaciones"("orden", "receta_id");

-- AddForeignKey
ALTER TABLE "Ingredientes" ADD CONSTRAINT "Ingredientes_receta_id_fkey" FOREIGN KEY ("receta_id") REFERENCES "recetas"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "preparaciones" ADD CONSTRAINT "preparaciones_receta_id_fkey" FOREIGN KEY ("receta_id") REFERENCES "recetas"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
