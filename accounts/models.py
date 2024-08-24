from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.conf import settings
user_model=settings.AUTH_USER_MODEL

class User(AbstractUser):
    email= models.EmailField(
        null=False,
        blank=False,
        unique=True
    )
    is_student= models.BooleanField(default=False,null=True)
    is_lecturer= models.BooleanField(default=False,null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=[]



class Profile(models.Model):
    user= models.OneToOneField(
        user_model,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=False
    )

    department=models.CharField(
        max_length=50,
        blank=False,
        null=False,
        help_text='Enter the name of your department'
    )
    faculty=models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='School or Faculty'
    )

    class Meta:
        abstract=True



class LecturerProfile(Profile):
    pass
    
class StudentProfile(Profile):
    matric_number=models.CharField(
        max_length=15,
        blank=False,
        null=False,

        )
    
    
    year_of_grad=models.DateField(
        verbose_name='Year of graduation',
        help_text='Choose estimated year of graduation',
        null=True,
        blank=False,
    )
    # supervisors=


