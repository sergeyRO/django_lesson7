from rest_framework import permissions


class OwnerHasRights(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return request.user.is_staff
        return request.user == obj.creator


class OwnerNotHasRights(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(f"OBJ===>     {obj}")
        print(f"REQ===>     {request}")
        return request.user == obj.creator
        # if request.user.is_staff:
        #     return request.user.is_staff
        # return request.user == obj.creator
