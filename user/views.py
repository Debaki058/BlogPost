from rest_framework.decorators import APIView
from django.http import JsonResponse
import base64
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from blogapp import global_msg
from .serializers import UserRegistrationSerializer


def login_data(request):
    error_list = []
    auth_headers = request.META.get('HTTP_AUTHORIZATION') #Basic sdfkjgkfghjklfgklfjksf
    
    if auth_headers:
        encoded_data = auth_headers.split(' ')[1] #['Basic', 'sdfkjgkfghjklfgklfjksf'] decoded_data = sdfkjgkfghjklfgklfjksf
        decoded_data = base64.b64decode(encoded_data).decode('utf-8').split(':') #username:password split garne bitikoi data list ma aauxa user name r passworde xurwea aauxa 0 r 1 index ma aauxa
        user_name = decoded_data[0]
        password = decoded_data[1]
        print(user_name)
        print(password)

        if user_name and password:
            try:
                user = User.objects.get(username=user_name) #debaki vanne user xa ki xain check garxa bahira bata yadi xa vane 
                db_password = user.password
                is_match_password = check_password(password, db_password)
                if not is_match_password:
                    error_list.append("Invalid Username and Password!")
                
            except User.DoesNotExist:
                error_list.append("No such user in Database!")
        else:
            error_list.append("Username and Password cannot be blank!")

    else:
        error_list.append("Authorization header missing!")

    return error_list, user_name, password    


class LoginApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        error_list, user_name, password = login_data(request)
        
        if error_list:
            return JsonResponse({"errors": error_list}, status=404)
        
        user = authenticate(request, username = user_name, password = password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            msg = {
                "username":user.username,
                "email":user.email,
                "token": token.key
            }
            return JsonResponse(msg, status = 200)
        
class UserRegisterApiView(APIView):
    
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'msg': 'User registered successfully'}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': 'Internal server error', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        


