import logging

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import APIView
from rest_framework import status
from rest_framework.authentication import BaseAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from blogapp.models import Student
from blogapp import global_msg
from blogapp.serializers import StudentSerializers


logger = logging.getLogger('django')

class StudentCreateApiView(APIView):
    authentication_classes = []
    permission_classes = []
    ''' This class creates a new student only.'''
    def post(self, request):
        if not request.body:
            msg = {
                global_msg.RESPONSE_CODE_KEY: global_msg.UNSUCCESS_RESPONSE_CODE,
                global_msg.RESPONSE_MSG_KEY: "Invalid Request Body!"
            }
            return JsonResponse(msg, status=status.HTTP_404_NOT_FOUND)

        try:
            error_list = []
            data = request.data
            serializers = StudentSerializers(data=request.data)
            user = User.objects.get(username='debaki')

            if serializers.is_valid():
                serializers.save(created_by=user)
                msg = {
                    global_msg.RESPONSE_CODE_KEY: global_msg.SUCCESS_RESPONSE_CODE,
                    global_msg.RESPONSE_MSG_KEY: "Success"
                }
                return JsonResponse(msg, status=status.HTTP_200_OK)

            msg = {
                global_msg.RESPONSE_CODE_KEY: global_msg.UNSUCCESS_RESPONSE_CODE,
                global_msg.RESPONSE_MSG_KEY: "Invalid Data",
                global_msg.ERROR_KEY: serializers.errors
            }
            return JsonResponse(msg, status=status.HTTP_400_BAD_REQUEST)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)
          

class StudentListApiView(APIView):
    authentication_classes=[TokenAuthentication]
    premission_classes=[IsAuthenticated]
    '''This class shows the all the list of student'''

    def get(self,request):
        print(request.headers)
        try: 
            student=Student.objects.all()#model instance
            serializers=StudentSerializers(student,many=True)#model instance to python
            
            msg={
                    global_msg.RESPONSE_CODE_KEY:global_msg.SUCCESS_RESPONSE_CODE,
                    global_msg.RESPONSE_MSG_KEY:"SUCESS OF  DATA ",
                    "data":serializers.data
                }
         
            return JsonResponse(msg, status = status.HTTP_200_OK)
            
        except Exception as exe:
            logger.error(str(exe),exc_info=True)
            
            msg={
                global_msg.RESPONSE_CODE_KEY:global_msg.UNSUCCESS_RESPONSE_CODE,
                global_msg.RESPONSE_MSG_KEY :"invalid  Data"
        }
        return JsonResponse(msg,status=status.HTTP_400_BAD_REQUEST)  
 

class StudentEditApiView(APIView): 
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 
    def put(self, request,pk):
        if not request.body:
            msg = {
                global_msg.RESPONSE_CODE_KEY: global_msg.UNSUCCESS_RESPONSE_CODE,
                global_msg.RESPONSE_MSG_KEY: "Edit Scucessfully.!"
            }
            return JsonResponse(msg, status=status.HTTP_200_OK)

        try:
            student = Student.objects.get(id=pk, is_delete=False) #id 1 ko details
            serializers = StudentSerializers(student, data=request.data)
            user = User.objects.get(username='devi')

            if serializers.is_valid():
                serializers.save(created_by=user)
                serializers.save
                
                msg = {
                    global_msg.RESPONSE_CODE_KEY: global_msg.SUCCESS_RESPONSE_CODE,
                    global_msg.RESPONSE_MSG_KEY: "Data Update Successfully"
                }
                return JsonResponse(msg, status=status.HTTP_200_OK)

            msg = {
                global_msg.RESPONSE_CODE_KEY: global_msg.UNSUCCESS_RESPONSE_CODE,
                global_msg.RESPONSE_MSG_KEY: "Invalid Data",
                global_msg.ERROR_KEY: serializers.errors
            }
            return JsonResponse(msg, status=status.HTTP_400_BAD_REQUEST)
        
        except ObjectDoesNotExist as exe:
            logger.error(str(exe), exc_info=True)
            msg = {
                global_msg.RESPONSE_CODE_KEY:global_msg.UNSUCCESS_RESPONSE_CODE,
                global_msg.RESPONSE_MSG_KEY:"No data Found!"
            }
            return JsonResponse(msg, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exe:
            logger.error(str(exe), exc_info=True)


class StudentDeleteApiView(APIView): 
    authentication_classes=[]
    permission_classes=[]
    '''This class delete all the  student'''
    def delete(self,request,id):
        
        try:
            print(id)
            student=Student.objects.get(id=id)
            student.is_delete = True
            student.save()
            msg={
                    global_msg.RESPONSE_CODE_KEY:global_msg.SUCCESS_RESPONSE_CODE,
                    global_msg.RESPONSE_MSG_KEY:"Delete sucessfully "
                }
            return JsonResponse(msg,status=status.HTTP_200_OK)
        except ObjectDoesNotExist as exe:
            logger.error(str(exe), exc_info=True)
            msg={
                global_msg.RESPONSE_CODE_KEY:global_msg.UNSUCCESS_RESPONSE_CODE,
                global_msg.RESPONSE_MSG_KEY :"Not Data Found"
            }   
            return JsonResponse(msg,status=status.HTTP_400_BAD_REQUEST)
        except Exception as exe:
            logger.error(str(exe), exc_info=True)
            msg={
                global_msg.RESPONSE_CODE_KEY:global_msg.UNSUCCESS_RESPONSE_CODE,
                global_msg.RESPONSE_MSG_KEY :" All Invalid Data"
            }
            return JsonResponse(msg,status=status.HTTP_400_BAD_REQUEST)
