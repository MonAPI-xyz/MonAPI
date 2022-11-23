from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from login.models import Team, TeamMember
from login.serializers import TeamSerializers
import os

class TeamManagementViewSet(mixins.CreateModelMixin,
							mixins.UpdateModelMixin,
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

	def update(self, request, *args, **kwargs):
		team = Team.objects.get(pk=kwargs['pk'])
		if (request.auth.team == team):
			if (request.data.get('name') is not None):
				return Response(data={"error": "Team name cannot be changed!"}, status=status.HTTP_400_BAD_REQUEST)
			
			# remove old image
			if (request.data.get('logo') is not None and team.logo and os.path.exists(team.logo.path)):
				os.remove(team.logo.path)
				team.logo = request.data.get('logo')

			if (request.data.get('description') is not None):
				team.description = request.data.get('description')
			
			team.save()

			serialized_obj = TeamSerializers(team)
			return Response(data=serialized_obj.data, status=status.HTTP_200_OK)
		else:
			return Response(data={"error": "Require to change team first!"}, status=status.HTTP_400_BAD_REQUEST)
			
		