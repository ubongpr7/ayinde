from django.contrib import admin
from .models import User,StudentProfile,LecturerProfile,Profile
# Register your models here.

admin.site.register(User)
admin.site.register(LecturerProfile)
admin.site.register(StudentProfile)
