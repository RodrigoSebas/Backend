from rest_framework import permissions

class EsAdministrador(permissions.BasePermission):
    #para cambiar el mensaje cuando falle
    message = 'Lo sentimos pero aca solo pueden ingresar administradores'
    def has_permission(self, request, view):
        print(view)
        tipo_usuario = request.user.tipoUsuario

        if tipo_usuario == 'ADMIN':
            return True
        else:
            return False
        
class EsNovio(permissions.BasePermission):
    message = 'Acceso solo valido para los novios'

    def has_object_permission(self, request, view):
        tipo_usuario = request.user.tipoUsuario

        if tipo_usuario == 'NOVIO':
            return True
        else:
            return False