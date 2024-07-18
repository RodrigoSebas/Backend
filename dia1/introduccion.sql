--comentario
--DDL(creacion de base de datos)
CREATE DATABASE pruebas;
--se recomienda el nombre de la tabla en plural
CREATE TABLE alumnos(
    id SERIAL NOT NULL PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellidos TEXT NULL,
    correo TEXT NOT NULL UNIQUE, --EL CORREO VA A SER UNICO
    matriculado BOOLEAN DEFAULT true,
    fecha_nacimiento DATE NULL
);

--DML(manejar los datos en la base de datos)
--\c nombre_db para cambiar de base de datos
--\l muestra todas las bases de datos que se tiene
--\dt muestra las tablas creadas
--las comillas simples es para ingresar datos en string en sql
INSERT INTO alumnos(id, nombre, apellidos, correo, matriculado, fecha_nacimiento) VALUES
(DEFAULT, 'Eduardo', 'de Rivero', 'ederiveroman@gmail.com', true, '1992-08-1');

INSERT INTO "alumnos" (nombre, "apellidos", correo, "matriculado", fecha_nacimiento) VALUES
                      ('Segundo', 'Alvarez', 'salvarez@gmail.com', true, '1995-09-18'),
                      ('Renzo', 'Soles Contreras', 'rsoles@hotmail.com', false, '2000-02-14'),
                      ('Abel', 'Guevara', 'aguevara@yahoo.es', true, '1989-10-08'),
                      ('Rodrigo','Trujillo Mirano', 'rtrujillo@gmail.com', false, '1998-05-19'),
                      ('Ignacion', 'Estremadoyro Lam', 'iestremadoyro@hotmail.com', true, '1990-06-17');


UPDATE "alumnos" SET "fecha_nacimiento" = '1995-06-17', matriculado = false
WHERE nombre = 'Abel' AND apellidos = 'Guevara';

DELETE FROM "alumnos" WHERE nombre='Shrek';

-- si queremos hacer una serie de pasos(o paso) que se puedean revertir debemos utilizar una transaccion

BEGIN;
DELETE FROM "alumnos" WHERE nombre='Eduardo';
--o bien se usa rollback o bien commit, rollback para regresar y commit para que los cambios perduren
ROLLBACK;
COMMIT;
--SAVEPOINT punto_guardado se guarda hasta ese momento exacto
--ROLLBACK to punto_guardado


--ejercicio
select * from alumnos where (nombre = 'Abel' or nombre='Renzo' ) and matriculado = false
--

--esto significa que devuelva todos los nombres que tengan la letra a en minuscula en su ontenido
select * from alumnos where nombre like '%a%'

--lo mismo de arriba pero que no sea sensibles a minusculas que revise todo
select * from alumnos where nombre ilike '%a%'

--lo mismo pero los guiones bajo representan posiciones en una palabra
select * from alumnos where nombre ilike '___a%'

--antepenultima letra sea a
select * from alumnos where nombre ilike '%a__'

--combinacion de caracteres
select * from alumnos where nombre ilike '%a__i%'

--para busquedas en varios datos
select * from alumnos where nombre in ('Abel','Rodrigo')

--orden
select * from alumnos order by nombre asc, apellidos desc;
select * from alumnos order by nombre desc;

--paginacion
--dice que limit es el numero maximo de filas que devolvera, con offset le decimos
--que cuantos elementos queremos que se salte, por ejemplo aqui muestra
--2 alumnos pero se salte a las dos primeras filas del conjunto total
select * from alumnos limit 2 offset 2