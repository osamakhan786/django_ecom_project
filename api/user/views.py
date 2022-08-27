from ast import Try
import email
import http
import imp
from lib2to3.pgen2 import token
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .models import CustomUser
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout

# Create your views here.
import random
import re

def generate_session_token(lenght=10):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]) for _ in range(lenght))

@csrf_exempt
def signin(request):
    if not request.method == 'POST':
        return JsonResponse({'error': 'send a post request with valid parameters'})
    
    username = request.POST['email']
    password = request.POST['password']
    
    if not re.match("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", username):
        return JsonResponse({'error': 'Enter a valid email'})
    
    if len(password) < 3:
        return JsonResponse({'error': 'password needs to be at least of 3 char'})
    
    
    UserModel = get_user_model()
    
    
    try:
        user = UserModel.objects.get(email=username)
        
        if user.check_passwaord(password):
            usr_dict = UserModel.objects.filter(email=username).values()
            usr_dict.pop('password')
            
            if user.session_token != "0":
                user.session_token = "0"
                user.save()
                return JsonResponse({'error': 'Previous session exists'})
            
            token = generate_session_token()
            user.session_token = token
            user.save()
            login(request , user)
            return JsonResponse({'token': token, 'user': usr_dict})
        else:
            return JsonResponse({'error': 'Invalied passwoed'})
            
    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'Invalid Email'})        
    
    
def signout(request , id):
    logout(request)
    
    UserMoodel = get_user_model()
    try:
        user = UserMoodel.objects.get(pk=id) 
        user.session_token = "0"
        user.save() 
        
    except UserMoodel.DoesNotExist:
        return JsonResponse({'error': 'Invalid user ID'})
    
    return JsonResponse({'success': 'Logout success'})  



class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create': [AllowAny]}
    serializer_class = UserSerializer    
    
    
    def get_permissions(self):
        try:
            return[permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]