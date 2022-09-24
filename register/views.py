from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status

from django.db.utils import IntegrityError
from register.serializers import RegistrationSerializer

@api_view(['POST', ])
@authentication_classes([])
@permission_classes([])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        try:
            user = serializer.save()
        except IntegrityError:
            data['response'] = 'User already registered! Please use a different email to register.'
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data['response'] = 'Successfully registered new user.'
        data['email'] = user.email
    else:
        data = serializer.errors
    if 'password' in data:
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    return Response(data, status=status.HTTP_201_CREATED)

