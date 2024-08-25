from django.contrib import admin
from .models import User,StudentProfile,LecturerProfile,Faculty,Department
# Register your models here.

admin.site.register(User)
admin.site.register(LecturerProfile)
admin.site.register(StudentProfile)
admin.site.register(Faculty)
admin.site.register(Department)
