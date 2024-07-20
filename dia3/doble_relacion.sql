-- sudo -u rodrigo pg_dump -f copia_seguridad.sql finanzas 
--lo de arriba es para hacer una copia de seguridad
--en lugar de .sql tambien se puede poner .backup
--pero se pone de otra manera 
-- sudo -u rodrigo pg_dump -F c -f copia_seguridad.backup finanzas 


--para restaurar en ubuntu se usa esto donde copia_seguridad  es el archivo sql y prueba la base de datos donde restauramos todo
--sudo -u rodrigo cat copia_seguridad.sql | psql -d prueba

--pg_restore solo se usa con archivos .backup
--para hacer la restauracion primero debemos tener la base de datos
--creada pero sin ninguna tabla

--para restaurar en .backup o sin extension donde prueba es el nombre de la base de datos y copia_seguridad el archivo con la copia de seguridad 
--sudo -u rodrigo pg_restore -d prueba -v copia_seguridad.backup



INSERT INTO movimientos (cuenta_origen, cuenta_destino, monto, fecha_transaccion) VALUES
(null, 1, 100.10, '2024-07-01T14:15:17'),
(null, 2, 500.20, '2024-07-06T09:30:15'),
(null, 3, 650.00, '2024-07-06T15:29:18'),
(null, 4, 456.00, '2024-07-08T10:15:17'),
(null, 5, 500.00, '2024-07-10T17:18:24'),
(null, 6, 1050.24, '2024-07-04T12:12:12'),
(null, 7, 984.78, '2024-07-09TT11:06:49'),
(1,2, 40.30, '2024-07-10T10:10:10'),
(4,7, 350.00, '2024-07-16T20:15:35'),
(3, null, 50.00, '2024-07-16T22:15:10'),
(5, null, 100.00, '2024-07-17T10:19:25'),
(6, null, 350.28, '2024-07-18T14:15:16');



SELECT *, 
CASE
    WHEN cuenta_origen IS NULL AND cuenta_destino IS NOT NULL THEN 'DEPOSITO'
    WHEN cuenta_origen IS NOT NULL AND cuenta_destino IS NULL THEN 'RETIRO'
    WHEN cuenta_origen IS NOT NULL AND cuenta_destino IS NOT NULL THEN 'TRANSFERENCIA'
    ELSE 'MOVIMIENTO DESCONOCIDO'
END AS tipo_movimiento 
FROM movimientos;

--ejercicio

select *, 
CASE
    when correo like '%@gmail.com%' then 'ES JOVEN'
    when correo like '%@yahoo.es%' then 'ES UN DINOSAURIO'
    when correo like '%@hotmail.com%' then 'ES ADULTO'
    ELSE 'CORREO DESCONOCIDO'
END AS tipo_edad
from clientes;


--ejercicio de hallar los saldos de las cuentas
-- lo que entra - lo que sale
-- Combinamos las dos consultas
WITH debitos AS (
    SELECT cuenta_origen AS cuenta, SUM(monto) AS debitos
    FROM movimientos
    WHERE cuenta_origen IS NOT NULL
    GROUP BY cuenta_origen
),
creditos AS (
    SELECT cuenta_destino AS cuenta, SUM(monto) AS creditos
    FROM movimientos
    WHERE cuenta_destino IS NOT NULL
    GROUP BY cuenta_destino
)
-- COALESCE es una funcion que acepta una lista de argumentos y retirna el primer elemento no nulo de la lista
SELECT COALESCE(debitos.cuenta, creditos.cuenta) AS cuenta, COALESCE(creditos.creditos, 0) - COALESCE(debitos.debitos, 0) AS saldo
FROM debitos
FULL OUTER JOIN creditos ON debitos.cuenta = creditos.cuenta 
ORDER BY cuenta;



