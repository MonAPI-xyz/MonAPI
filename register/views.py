import os

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status

from django.db.utils import IntegrityError
from register.serializers import RegistrationSerializer, VerifiedUserTokenSerializer
from login.models import Team, TeamMember
from register.models import VerifiedUser, VerifiedUserToken

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist

@api_view(['POST', ])
@authentication_classes([])
@permission_classes([])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        try:
            user = serializer.save()
            username = user.username.split('@')[0]
            team = Team.objects.create(name=username.title())
            TeamMember.objects.create(user=user, team=team, verified=True)
            verified_user = VerifiedUser.objects.create(user=user)
            token = VerifiedUserToken.objects.create(verified_user=verified_user)
            verify_url = f"{os.environ.get('FRONTEND_URL', '')}/verify?key={token.key}"

            email_content = f'''
                        To verify your registration on MonAPI, please follow the link below.\n
                        If you did not register on MonAPI, you can ignore this email. \n\n
                        {verify_url}
                        '''

            email_content_html = render_to_string('email/verify_email.html', {
                'verify_url': verify_url,
            })

            send_mail(
                f'MonAPI User Verification',
                email_content,
                None,
                [user.email],
                html_message=email_content_html,
                fail_silently=False,
            )

        except IntegrityError:
            data['response'] = 'User already registered! Please use a different email to register.'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        data['response'] = 'Successfully registered new user.'
        data['email'] = user.email
    else:
        data = serializer.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    return Response(data, status=status.HTTP_201_CREATED)

@api_view(['POST', ])
@authentication_classes([])
@permission_classes([])
def verify_view(request):
    serializer = VerifiedUserTokenSerializer(data=request.data)
    if serializer.is_valid():
        try:
            verified_user = VerifiedUserToken.objects.get(key=serializer.validated_data['key']).verified_user
            verified_user.verified = True
            verified_user.save()
            data = {'response': 'Success'}
            return Response(data=data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            data = {'response': 'Token is invalid.'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = {'response': 'Pass a valid token.'}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


