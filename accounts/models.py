from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.
from django.conf import settings
user_model=settings.AUTH_USER_MODEL

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

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
    objects=CustomUserManager()
    
    def save(self, *args, **kwargs):
        self.username=self.email

        super().save(*args, **kwargs)


class Faculty(models.Model):
    name=models.CharField(
        max_length=50,
        blank=False,
        null=False,
        help_text='Enter the name of  deartment'
    )

class Department(models.Model):
    name=models.CharField(
        max_length=50,
        blank=False,
        null=False,
        help_text='Enter the name of  deartment'
    )
    faculty=models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name='departments'
    )

class Profile(models.Model):
    user= models.OneToOneField(
        user_model,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=False
    )

    department=models.ForeignKey(
        Department,
        blank=False,
        null=True,
        help_text='Choose your department',
        on_delete=models.SET_NULL

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


