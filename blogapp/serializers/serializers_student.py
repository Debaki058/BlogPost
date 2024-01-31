from rest_framework import serializers
from blogapp.models import Student




    
class StudentSerializers(serializers.Serializer):
        studentName = serializers.CharField(source ='name',error_messages={"blank":"Name can not be blank!"})
        studentAddress = serializers.CharField(source ='address',
                                            error_messages={"blank":"address can not be blank!"})
        studentAge = serializers.IntegerField(source ='age',
                                        error_messages={"blank":"Age can not be blank!"})
        mobileNumber = serializers.CharField(source ='mobile_number', 
                                            error_messages={"blank":"Mobile Number can not be blank!"})
        rollNumber = serializers.IntegerField(source ='roll_number',
                                        error_messages={"blank":"Roll Number can not be blank!"})
        

        def create(self,validated_data):
            return Student.objects.create(**validated_data)  


        def update(self,instance,validate_data):
            instance.name=validate_data.get('name',instance.name)
            instance.address=validate_data.get('address',instance.address)
            instance.age=validate_data.get('age',instance.age)
            instance.mobile_number=validate_data.get('mobile_number',instance.mobile_number)
            instance.roll_number=validate_data.get('roll_number',instance.roll_number)
            instance.save()
            return instance
            
        def validate_studentAge(self, age):
            if age<0 or age>110:
                raise serializers.ValidationError(f"Invalid age.your age is {age}")
            return age


        def validate_mobileNumber(self, mobile_number):
            if len(mobile_number) != 10:
                raise serializers.ValidationError(f"Mobile Number Must be 10 digit length.it contain {len(mobile_number)}!")
            else:
                if self.instance: # for update 
                    if Student.objects.filter(mobile_number=mobile_number).exclude(id = self.instance.id).exists():
                        raise serializers.ValidationError("Mobile Number Already Exist!")
                    else:
                        if Student.objects.filter(mobile_number=mobile_number).exists():
                            raise serializers.ValidationError("Mobile Number Already Exist!")
                        
            return mobile_number
                    
          
       