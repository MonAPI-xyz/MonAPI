from datetime import timedelta
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import views, status
from rest_framework.response import Response

from forget_password.models import ForgetPasswordToken
from forget_password.serializers import RequestForgetPasswordTokenSerializer, ResetPasswordSerializer, ForgetPasswordTokenCheckSerializer

import os


class RequestForgetPasswordTokenView(views.APIView):
    authentication_classes = []
    permission_classes = []
    
    def get(self, request, format=None):
        serializer = ForgetPasswordTokenCheckSerializer(data=request.query_params)
        if serializer.is_valid():
            tokens = ForgetPasswordToken.objects.filter(
                key=serializer.validated_data['key'], 
                created_at__gte=timezone.now() - timedelta(hours=1)
            )
            if len(tokens) == 0:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': True})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

    def post(self, request, format=None):
        serializer = RequestForgetPasswordTokenSerializer(data=request.data)
        if serializer.is_valid():
            users = User.objects.filter(email=serializer.validated_data['email'])
            if len(users) == 0:
                return Response({'error': 'User not exists with given email'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = users[0]
            token = ForgetPasswordToken.objects.create(user=user)
            
            reset_url = f"{os.environ.get('FRONTEND_URL', '')}/forget_password?key={token.key}"
            
            email_content = f'''
            We have received a password reset request for your email.\n
            Please follow below link to create new password for your account. \n\n
            {reset_url}
            This link is valid for 1 hours.
            '''
            
            email_content_html = render_to_string('email/reset_password.html', {
                'reset_url': reset_url,
            })
            
            send_mail(
                'MonAPI Reset Password Request',
                email_content,
                'MonAPI <noreply@monapi.xyz>',
                [user.email],
                html_message=email_content_html,
                fail_silently=False,
            )   
            
            return Response({'success': True})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ResetPasswordView(views.APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            tokens = ForgetPasswordToken.objects.filter(
                key=serializer.validated_data['key'], 
                created_at__gte=timezone.now() - timedelta(hours=1)
            )
            if len(tokens) == 0:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
            
            token = tokens[0]
            user = token.user
            
            check_password = user.check_password(serializer.validated_data['password'])
            if check_password:
                return Response({'error': 'Please choose password that different from your current password'}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['password'])
            user.save()
            
            token.delete()
            
            return Response({'success': True})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
