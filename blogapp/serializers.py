from rest_framework import serializers
from .models import Student

class TestSerializers(serializers.Serializer):
    name = serializers.CharField(error_messages = {"blank":"Name can not be blank."})
    address = serializers.CharField(error_messages = {"blank":"Address can not be blank."})
    age = serializers.IntegerField(error_messages = {"blank":"age can not be blank."})
    mobile_number = serializers.CharField(error_messages = {"blank":"mobile_number can not be blank."})
    


    def create(self, validated_data):
        print('validate data', validated_data)
        return Student.objects.create(**validated_data)
    

    def update(self, instance, validated_data):
        validated_data = {"name":"Debaki", "address":"Hetauda"}
        #instance means existing data
        instance.name = validated_data.get ('name', instance.name)

    def validate_age(self,age):
            if age>100 or age<0:
                raise serializers.ValidationError("Age must be valid in range 1 to 100.")  

            return age  
    
    def validate_mobile_number(self, value):#value = mobile_number
         print('dddddddddd',value)
         if Student.objects.filter(mobile_number=value).exists():
              raise serializers.ValidationError("Mobile number Already Exist!")  
         return value
              
            

    














