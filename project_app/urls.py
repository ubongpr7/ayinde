from django.urls import path
from .views import *
urlpatterns=[
    path('',home,name='home'),
    path('update/<str:app_name>/<str:model_name>/<int:pk>/', GenericUpdateView.as_view(), name='generic_update'),
    path('add/<str:app_name>/<str:model_name>/<int:project_id>/', CommentGradeCreateView.as_view(), name='generic_create'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('project/new/', create_or_update_project, name='create_project'),
    path('project/edit/<int:project_id>/', create_or_update_project, name='edit_project'),
]