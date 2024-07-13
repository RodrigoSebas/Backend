nombre = "Rodrigo"

edad = 22
edad = [121,21,212]
print(len(edad))


# args son parametros multiples que se printean como tupla, kwargs es un diccionario
def combinada(*args, **kwargs):
    print(args)
    print(kwargs)

combinada(1,2,3,4,nombre="rodrigo",apellido="trujillo")
