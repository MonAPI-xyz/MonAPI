from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status

from login.serializers import LoginSerializer
from .utils import generate_token

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def user_login(request):
    data = {}
    serializer = LoginSerializer(data=request.data)
    
    serializer.validate_attribute(request.data)
    if serializer.is_valid():
        user = authenticate(request=request,
                            username=request.data['email'], 
                            email=request.data['email'], 
                            password=request.data['password'])
        if not user:
            data['response'] = 'Invalid email or password.'
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)   

        data['response'] = 'Sign-in successful.'
        data['email']= user.email
        data['token']= generate_token(user)
        
        return Response(data=data, status=status.HTTP_200_OK)
    else:
        data['response'] = 'Invalid email or password.'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)            
    
