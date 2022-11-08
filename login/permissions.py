from rest_framework.permissions import BasePermission
from rest_framework import status

class UserTeamExists(BasePermission):
    message = 'Invalid user team.'
    code = status.HTTP_400_BAD_REQUEST
    
    def has_permission(self, request, view):
        return request.auth.team != None