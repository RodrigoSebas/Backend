-- crear database
-- \! clear limpiar la terminal en psql
CREATE DATABASE finanzas;

CREATE TYPE enum_status as ENUM ('TIPO_A', 'TIPO_B', 'TIPO_C');
CREATE TABLE clientes(
    id SERIAL NOT NULL PRIMARY KEY,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL UNIQUE, --EL CORREO VA A SER UNICO
    status enum_status NOT NULL DEFAULT 'TIPO_A',
    activo BOOLEAN DEFAULT true,
    fecha_nacimiento TIMESTAMP DEFAULT NOW()
);

INSERT INTO clientes (nombre, correo, status, activo) VALUES
('Rodrigo Juarez Quispe', 'rjuarez@gmail.com', 'TIPO_A', true),
('Mariana Sanchez Gil', 'msanchez@hotmail.com', 'TIPO_B', true),
('Juliana Taco Martinez', 'jtaco@gmail.com', 'TIPO_A', true),
('Gabriel Gonza Perez', 'ggonza@yahoo.es', 'TIPO_C', false);

-- Funciones de agregacion
-- promedio > avg(Columna_numerica)
--minimo > min(Columna_numerica)
-- maximo > max(Columna_numerica)
-- contar > count(columna o registro cualquiera)

--ejemplo
SELECT MAX(id) FROM clientes;

-- si usamos a parte de la funcion de agregacion otra columna, nos vemos obligados a usar group by

select count(id), correo from clientes group by correo

-- cuantos usuarios estan activos o no. aqui lo del count(id o cualquier otra cosa) es irrelevante
-- a veces se pone count(*) porque no interesa lo que vaya ahi, no siempre es asi
select count(*), activo from clientes group by activo

--CUANTOS CLIENTES SON DEL TIPO_A O TIPO_B
select count(*), status 
from clientes 
where status='TIPO_A' OR status='TIPO_B' 
group by status 
order by count(*) desc;

--nueva tabla
CREATE TYPE enum_tipo_moneda as ENUM ('SOLES', 'DOLARES', 'EUROS');
create table cuentas(
    id serial not null primary key,
    numero_cuenta text not null unique,
    tipo_moneda enum_tipo_moneda not null,
    fecha_creacion timestamp default now(),
    mantenimiento float null,
    cliente_id int not null,
    --creo la relacion
    constraint fk_clientes foreign key(cliente_id) references clientes(id)
);

INSERT INTO cuentas (numero_cuenta, tipo_moneda, fecha_creacion, mantenimiento, cliente_id) VALUES
('0f302b7e-41b6-45e9-950c-d2640f3ddcdf', 'SOLES', '2023-10-08T10:05', '1.5', '1'),
('7160f103-dc2a-4e67-9123-3d795bf4938b', 'SOLES', '2024-02-01T14:23', '1', '2'),
('b2eeb8ab-f06b-49df-8dac-332b2b48d7ff', 'DOLARES', '2020-12-08T16:17', '0', '1'),
('82c51e22-f4a6-4430-b401-05e458979c1b', 'SOLES', '2022-05-14T09:45', '1', '3'),
('57c54a3c-0a92-45b7-b888-0cbf827c93f8', 'SOLES', '2024-03-14T11:28', '1.2', '4'),
('c62ed24c-430b-462f-bdb3-ba79199bcffc', 'EUROS', '2023-10-04T12:27', '0.5', '3'),
('2343b92e-152a-4316-a4af-7406f8e551b8', 'SOLES', '2023-11-09T11:11', '0', '2');


-- Cuantas cuentas hay en soles, dolares y euros

select count(*), tipo_moneda from cuentas group by tipo_moneda;

-- Mostrar los numeros de cuenta y su tipo de moneda ordenados por la fecha de creacion del mas nuevo al mas viejo

select numero_cuenta, tipo_moneda, fecha_creacion from cuentas order by fecha_creacion asc;

-- Cual es la cuenta con mayor mantenimiento 

select max(mantenimiento) from cuentas;

-- Que cliente tiene mas cuentas

select count(*), cliente_id from cuentas group by cliente_id order by count(*) desc;


INSERT INTO clientes (nombre, correo, status, activo) VALUES
('Eduardo de Rivero Manrique', 'ederivero@gmail.com', 'TIPO_B', true);





