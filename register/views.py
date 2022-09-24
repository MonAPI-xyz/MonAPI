from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from register.serializers import RegistrationSerializer

@api_view(['POST', ])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        data['response'] = 'Successfully registered new user.'
        data['email'] = user.email
        data['status_code'] = 201
    else:
        data = serializer.errors
    return Response(data, status=status.HTTP_201_CREATED)

