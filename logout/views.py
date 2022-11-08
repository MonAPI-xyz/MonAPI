from django.contrib.auth import logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_logout(request):
    request.auth.delete()
    logout(request)

    return Response('User Logged out successfully')
