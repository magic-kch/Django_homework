from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешить чтение всем
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Разрешить изменение и удаление только создателю объекта
        return obj.creator == request.user


class IsAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff
