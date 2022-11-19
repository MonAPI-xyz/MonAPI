from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from login.models import Team, TeamMember
from login.serializers import TeamSerializers
from team_management.serializers import TeamManagementSerializers
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

class TeamManagementViewSet(mixins.CreateModelMixin,
							viewsets.GenericViewSet):

	queryset = Team.objects.all()
	serializer_class = TeamSerializers
	permission_classes = [IsAuthenticated]
	lookup_field = "pk"

	def get_team_data_from_request(self, request):
		team_data = {
			'name': request.data.get('name'),
			'description': request.data.get('description', '-'),
			'logo': request.data.get('logo'),
		}
		return team_data
		
	def create(self, request, *args, **kwargs):
		team_data = self.get_team_data_from_request(request)
		team_serializer = TeamSerializers(data=team_data)
		if team_serializer.is_valid():
			new_team = Team.objects.create(**team_data)
			TeamMember.objects.create(team=new_team, user=request.user)
			serialized_obj = TeamSerializers(new_team)
			return Response(data=serialized_obj.data, status=status.HTTP_201_CREATED)
			
		return Response(data={"error": "Please make sure your [team name] is exist!"}, status=status.HTTP_400_BAD_REQUEST)

	@action(detail=False,methods=["GET"])
	def current(self, request):
		serializer = TeamManagementSerializers(request.auth.team)
		return Response(serializer.data)
		

