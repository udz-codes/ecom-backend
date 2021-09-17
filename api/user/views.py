import random
import re
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .models import CustomUser
from django.contrib.auth import get_user_model, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


def generate_session_token(length=10):
    """
    Generating alpha-numeric random token of given length.
    """

    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]) for _ in range(length))


@csrf_exempt
def signin(request):

    if not request.method == "POST":
        return JsonResponse({'error': 'Send a post request with valid parameters only'})

    username = request.POST['email']
    password = request.POST['password']

    if not re.match("[\w\.-]+@[\w\.-]+\.\w{2,4}", username):
        return JsonResponse({'error': 'Please enter a valid email address'})
    
    if len(password) < 8:
        return JsonResponse({'error': 'Password length needs to be atleast 8 characters'})

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(email=username)

        if user.check_password(password):
            user_dict = UserModel.objects.filter(email=username).values().first()
            user_dict.pop('password')

            if user.session_token != "0":
                user.session_token = "0"
                user.save()
                return JsonResponse({'error': 'A session already exists'})
            
            token = generate_session_token()

            user.session_token = token
            user.save()
            
            login(request, user)
            return JsonResponse({'token': token, 'user': user_dict})
        else:
            return JsonResponse({'error': 'Invalid Password'})

    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'Invalid Email'})


def signout(request, id):
    
    UserModel = get_user_model()
    
    try:
        user = UserModel.objects.get(pk=id)
        user.session_token = "0"
        user.save()

        logout(request)
        return JsonResponse({'success': 'Logout success'})

    except UserModel.DoesNotExist():
        return JsonResponse({'error': 'Invalid user ID'})


class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create': [AllowAny]}

    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]