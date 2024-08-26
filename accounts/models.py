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


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username

class Faculty(models.Model):
    name=models.CharField(
        max_length=50,
        blank=False,
        null=False,
        help_text='Enter the name of  deartment'
    )

    def __str__(self):
        return self.name

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
    def __str__(self):
        return self.name

class Profile(models.Model):
    user= models.OneToOneField(
        user_model,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        editable=False,
    )
    

    department=models.ForeignKey(
        Department,
        blank=False,
        null=True,
        help_text='Choose your department',
        on_delete=models.SET_NULL

    )
    def __str__(self):
        if self.user.first_name:
            return f'{self.user.first_name} {self.user.last_name}'
        return f'{self.user.email}'
        
    

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
    
    
    graduation_year=models.DateField(
        verbose_name='Year of graduation',
        help_text='Choose estimated year of graduation',
        null=True,
        blank=False,
    )
    # supervisors=


