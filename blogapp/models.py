from django.db import models
import uuid
from django.contrib.auth.models import User


# Create your models here.
def uuid_generate():
  return uuid.uuid4().hex

class BaseModel(models.Model):
    reference_id = models.CharField(max_length=32, unique=True, default=uuid_generate)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, db_column="created_by", null=True,related_name="+")
    created_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, db_column="updated_by", null=True,related_name="+")
    updated_at =  models.DateTimeField(null=True)
    is_delete = models.BooleanField(default=False)


    class Meta:
        abstract = True 


class Student(BaseModel):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    age = models.IntegerField()
    mobile_number = models.CharField(max_length=10)
    roll_number = models.IntegerField()

    class Meta:
        db_table = 'student'
        managed = False #postgrey bata banayako table 
        
class Course(BaseModel):
    name = models.CharField(max_length=100)
    pub_date = models.DateField(null=True)
    page = models.IntegerField()

    class Meta:
        db_table = 'course'



                