from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, logout
from rest_framework import status

from login.serializers import LoginSerializer, TeamSerializers
from login.models import TeamMember, Team
from login.utils import generate_token

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def user_login(request):
    data = {}
    serializer = LoginSerializer(data=request.data)
    
    serializer.validate_attribute(request.data)
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
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_logout(request):
    request.auth.delete()
    logout(request)

    return Response('User Logged out successfully')


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_team(request):
    serializers = TeamSerializers(request.auth.team)
    return Response(serializers.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def available_team(request):
    team = Team.objects.filter(teammember__user=request.user)
    serializer = TeamSerializers(team, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_team(request):
    if 'id' not in request.data:
        return Response({'error': 'Team id required'}, status=status.HTTP_400_BAD_REQUEST)

    team_member = TeamMember.objects.filter(user=request.user, team__id=request.data['id'])
    if len(team_member) < 1:
        return Response({'error': 'Invalid team id'}, status=status.HTTP_400_BAD_REQUEST)
    
    auth = request.auth
    auth.team_member = team_member[0]
    auth.save()
    
    return Response({'success': True})

    