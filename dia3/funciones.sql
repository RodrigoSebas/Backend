create table demostracion_triggers (
    id serial primary key not null,
    contador int
);

--se pueden instalar extensiones
create extension if not exists "uuid-ossp";

-- funcion
create or replace function insertar_clientes_con_cuenta(nombre_cliente text, correo_cliente text, status_cliente enum_status, activo_cliente boolean, tipo_moneda enum_tipo_moneda)
returns void as $$
declare
    nuevo_cliente_id int;
--inicia la ejecucion de la funcion
begin
--returning retorna informacion si es un insert, update o delete
    --inicia la transaccion
    begin
    insert into clientes (nombre, correo, status, activo) values 
    (nombre_cliente, correo_cliente, status_cliente, activo_cliente)
    returning id into nuevo_cliente_id;

    insert into cuentas(numero_cuenta, tipo_moneda, cliente_id) values(uuid_generate_v4(), tipo_moneda, nuevo_cliente_id);
    commit;
    --si hay error
    exception
        when others then -- no nos fijamos en el error que tenemos, solo basta que tengamos un errror
            rollback;
    end; --finaliza la transaccion
end; -- finaliza la funcion
$$ language plpgsql;

select insertar_clientes_con_cuenta('shrek','shrek@dreamworks.com','TIPO_B', true, 'SOLES');



-- crear un trigger
create or replace function incrementador()