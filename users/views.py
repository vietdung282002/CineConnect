# Create your views here.
import logging

logger = logging.getLogger(__name__)

from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
import smtplib
from email.mime.text import MIMEText
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .permission import IsOwnerOrReadOnly
import random
from .models import CustomUser,UpdatePasswordToken
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserLogoutSerializer
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import os 


class UserRegisterViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    http_method_names = ['post']

    def create(self, request, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "status": "success",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        error_messages = ', '.join(sum(serializer.errors.values(), []))
        data = {
            "status": "error",
            "message": error_messages
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class UserLoginViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserLoginSerializer
    http_method_names = ['post']

    def create(self, request, **kwargs):
        username = request.data.get('username_or_email')
        password = request.data.get('password')
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:

            try:
                user = CustomUser.objects.get(email=username)
                username = user.username
            except CustomUser.DoesNotExist:
                data = {
                    "status": "error",
                    "message": "Such user was not found"
                }
                return Response(data,
                                status=status.HTTP_404_NOT_FOUND)

        # check to see if username with that password exist
        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            data = {
                "status": "success",
                "data": {
                    "token": token.key,
                    'id': user.id
                }
            }
            return Response(data, status=status.HTTP_200_OK)
        data = {
            "status": "error",
            "message": "Invalid credentials"
        }
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserLogoutSerializer
    http_method_names = ['post']
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, **kwargs):

        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            data = {
                "status": "success",
                "message": "Successfully logged out."
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data = {
                "status": "error",
                "message": str(e)
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_random_token(length):
    """
        Generate a random string, if length characters
    """
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    token = ""
    for i in range(length):
        index = random.randint(0, len(characters) - 1)
        token += characters[index]
    
    return token

def send_password_token(email, new_token):
    subject = ' Reset password '
    body = 'Use this pin: '+ new_token + 'to reset your password. It will expires in 15 mins'
    sender = os.environ.get('EMAIL_HOST_USER')
    recipient_list = [email]
    password = os.environ.get('EMAIL_HOST_PASSWORD')
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipient_list)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.ehlo()
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipient_list, msg.as_string())
        smtp_server.close()
    
@csrf_exempt
@api_view(['POST', ])
def request_password_update(request):
    """
        This endpoint takes in a email and check if a user with that email exist.
        If the user exist, send an email with a pin
    """

    #make sure the request has an email attached 
    try:
        user_email = request.data['email']
    except KeyError:
        data = {
                "status": "error",
                "message":'Invalid request'
            }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    #if a user with this email is found
    try:
        user = CustomUser.objects.get(email=user_email)
        #make sure user that not have an update token, if it has remove it
        try:
            password_token = UpdatePasswordToken.objects.get(user=user)
        except:
            password_token = UpdatePasswordToken(
                user=user,
                token=''
            )

        #generate new token and send email with the token
        new_token = get_random_token(10)
        password_token.token = new_token
        password_token.created_at = timezone.now()
        password_token.save()

        try:
            send_password_token(user_email, new_token)
        except Exception as e:
            data = {
                "status": "error",
                "message": str(e)
            }
            return Response(data=data, status=status.HTTP_417_EXPECTATION_FAILED)

        #return a success message
        return Response(data={'success': "success", 'message': 'Email have been sent to user'}, status=status.HTTP_200_OK)


    except CustomUser.DoesNotExist:
        return Response(data={'success': "error" ,'message': 'User was not found'}, status=status.HTTP_404_NOT_FOUND)
        #just return a failure message
  
@csrf_exempt        
@api_view(['POST'])
def confirm_user_passcode(request):
    """
        Confirming the user enter correct passcode to recover their emails
    """
    try:
        user_email = request.data['email']
        passcode = request.data['passcode']
    except:
        data = {
                "status": "error",
                "message":'This is a bad reqeust'
            }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    try:
        current_user = CustomUser.objects.get(email=user_email)
    except CustomUser.DoesNotExist:
        data = {
                "status": "error",
                "message":'This user does not exist'
            }
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    try:
        password_token = UpdatePasswordToken.objects.get(user=current_user)
        if password_token.is_valid() and password_token.token == passcode:
            password_token.delete()
            data = {
                "status": "success",
                "message": "passcode was valid"
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            data = {
                "status": "error",
                "message":'passcode was invalid'
            }
            password_token.delete()
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    except UpdatePasswordToken.DoesNotExist:
        data = {
                "status": "error",
                "message":'passcode did not match'
            }
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    
    
@csrf_exempt    
@api_view(['PUT', ])
def reset_password(request):
    """
        Reset password of user
    """
    try:
        new_password = request.data['newPassword']
        email = request.data['email']
    except KeyError:
        data = {
                "status": "error",
                "message":'This was an invalid request'
            }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        current_user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        data = {
                "status": "error",
                "message":'This user does not exist'
            }
        return Response(data={'message': 'This user does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    current_user.set_password(new_password)
    current_user.save()

    token, _ = Token.objects.get_or_create(user=current_user)


    data ={
                "status": "success",
                "message":'reset password successfull'
            }

    return Response(data=data, status=status.HTTP_200_OK)

@csrf_exempt    
@api_view(['PUT', ])
@permission_classes([permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly])
def change_password(request):
    """
        Reset password of user
    """
    try:
        current_password = request.data['currentPassword']
        new_password = request.data['newPassword']
        id = request.user.id
    except KeyError:
        data = {
                "status": "error",
                "message":'This was an invalid request'
            }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        current_user = CustomUser.objects.get(id=id)
    except CustomUser.DoesNotExist:
        data = {
                "status": "error",
                "message":'This user does not exist'
            }
        return Response(data={'message': 'This user does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    user = authenticate(username= current_user.username,password= current_password)
    if user:
        current_user.set_password(new_password)
        current_user.save()
    else:
        data = {
                "status": "error",
                "message":'wrong password'
            }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    data ={
                "status": "success",
                "message":'change password successfull'
            }

    return Response(data=data, status=status.HTTP_200_OK)