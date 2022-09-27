from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from login.serializers import LoginSerializer

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def user_login(request):
    data = {}
    serializer = LoginSerializer(data=request.data)
    
    serializer.validate_attribute(request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']

        data['response'] = 'Sign-in successful.'
        data['email']= user.email
        data['token']= generate_token(user)
        
        return Response(data=data, status=status.HTTP_200_OK)
    else:
        data['response'] = 'Invalid email or password.'
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)            
    
def generate_token(user):
    token, created = Token.objects.get_or_create(user=user)
    return token.key