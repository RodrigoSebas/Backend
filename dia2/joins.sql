select * from clientes inner join cuentas 
on clientes.id = cuentas.cliente_id 

select * from clientes left join cuentas 
on clientes.id = cuentas.cliente_id 

-- Devolver la informacion ( nombre, correo, status, numero_cuenta, tipo_moneda)

select nombre, correo, status, numero_cuenta, tipo_moneda from clientes inner join cuentas
on clientes.id = cuentas.cliente_id

-- Devolver la informacion de los usuarios que tengan cuenta que no sea en soles (nombre, correo)

select nombre, correo from clientes inner join cuentas
on clientes.id = cuentas.cliente_id where tipo_moneda != 'SOLES';

-- Devolver el usuario que tenga mantenimiento mas alto y que tipo de moneda es su cuenta

select nombre, mantenimiento, tipo_moneda from clientes inner join cuentas
on clientes.id = cuentas.cliente_id order by mantenimiento desc limit 1;

--crear tabla
--id primary key no nulo
-- cuenta_origen relacion con la tabla cuentas puede ser null
-- cuenta_destino relacion con la tabla cuentas no puede ser null
-- monto float no puede ser null
-- fecha_operacion timestamp la hora del servidor por defecto

create table movimientos(
    id serial primary key not null,
    cuenta_origen int,
    cuenta_destino int not null,
    monto float not null,
    fecha_operacion timestamp default now(),
    --relaciones
    constraint fk_cuenta_origen foreign key(cuenta_origen) references cuentas(id),
    constraint fk_cuenta_destino foreign key(cuenta_destino) references cuentas(id)
);

-- asi se puede alterar una tabla sin eliminarla
alter table movimientos alter column cuenta_destino drop not null;

--esto es para cambiar el nombre de la columna de una tabla
alter table movimientos rename column fecha_operacion to fecha_transaccion;
