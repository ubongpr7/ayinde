from django import forms
from .models import Project
from .models import Comment, Grade

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'document']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['score', 'feedback']
