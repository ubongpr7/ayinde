from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

from accounts.models import LecturerProfile

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    document = models.FileField(upload_to='projects/documents/')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    submitted_at = models.DateTimeField(auto_now_add=True)
    supervisors=models.ManyToManyField(
        LecturerProfile,
        related_name='projects',
        help_text='Hold shift and click to select multiple lecturers'
    
    )
    def __str__(self):
        return self.title



class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    supervisor = models.ForeignKey(LecturerProfile,null=True, on_delete=models.SET_NULL, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.supervisor.username} on {self.project.title}"

class Grade(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='grade')
    supervisor = models.ForeignKey(LecturerProfile,null=True,blank=True, on_delete=models.SET_NULL, related_name='grades')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField(blank=True, null=True)
    graded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Grade for {self.project.title} by {self.supervisor.username}"
