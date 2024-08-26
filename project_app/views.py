from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView
from django.forms import modelform_factory
from django.apps import apps
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Project, Comment, Grade
from .forms import CommentForm, GradeForm, ProjectForm

# Create your views here.

def home(request):
    
    return render(request,'index.html',)

# Generic Update View
class GenericUpdateView(UpdateView,LoginRequiredMixin):
    template_name = 'create.html'
    success_url = '/'

    def get_model(self):
        model_name = self.kwargs['model_name']
        app_name = self.kwargs['app_name']
        return apps.get_model(app_name, model_name)

    def get_object(self):
        model = self.get_model()
        return model.objects.get(pk=self.kwargs['pk'])

    def get_form_class(self):
        return modelform_factory(self.get_model(), fields='__all__')

    

    def form_valid(self, form):
            form.save()
            context = self.get_context_data(form=form)
            return self.render_to_response(context)

    def form_invalid(self, form):
        return super().form_invalid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        
        return context

# Generic Create View
class CommentGradeCreateView(CreateView,LoginRequiredMixin):
    template_name = 'create.html'
    success_url = '/'
    
    def get_model(self):
        model_name = self.kwargs['model_name']
        app_name = self.kwargs['app_name']
        return apps.get_model(app_name, model_name)

    def get_form_class(self):
        if self.kwargs['model_name']=='comment':
            return CommentForm
        elif self.kwargs['model_name']=='grade':
            return GradeForm



    def form_valid(self, form):
            project=get_object_or_404( Project,id=self.kwargs['project_id'])
            if self.request.user.is_lecturer:
                print(self.request.user.lecturerprofile)
                if self.request.user.lecturerprofile and self.kwargs['model_name'] in ['comment','grade']  :
                
                    form.instance.supervisor = self.request.user.lecturerprofile
                    form.instance.project = project
                    context = self.get_context_data(form=form)
                    response = super().form_valid(form)
                    
                else:
                    return redirect('/')
            return redirect('/')


    def form_invalid(self, form):
        return super().form_invalid(form)
       
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()

        context['title'] =f"Create {self.kwargs['model_name'].title()}"
        context['model_name'] =self.kwargs['model_name']
        context['app_name'] =self.kwargs['app_name']
        return context

@login_required
def create_or_update_project(request, project_id=None):
    if request.user.is_student:
        if project_id:
            # If a project_id is provided, we're editing an existing project
            project = get_object_or_404(Project, id=project_id)
            if project.student != request.user.studentprofile:
                return HttpResponseForbidden("You do not have permission to edit this project.")
        else:
        # Otherwise, we're creating a new project
            project = None
    else:
        messages.info(request,'You cannot create  or edit project')
        return redirect('/')
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if request.user.is_student:
            if form.is_valid():
                project = form.save(commit=False)
                if not project_id:  # If it's a new project, assign the student profile
                    project.student = request.user.studentprofile
                project.save()
                form.save_m2m()  # Save many-to-many relationships like 'supervisors'
                return redirect('project_detail', pk=project.id)
        else :
            messages.info(request,'You cannot create a project')
            return redirect('/')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'create.html', {'form': form,'title':"Submit Project"})



@method_decorator(login_required, name='dispatch')
class ProjectDetailView(FormMixin, DetailView):
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'
    form_class = CommentForm  # FormMixin will use this for comments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['grade_form'] = GradeForm()
        context['comments'] = Comment.objects.filter(project=self.object)
        context['grade'] = Grade.objects.filter(project=self.object).first()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'comment_submit' in request.POST:
            return self.handle_comment_form(request)
        elif 'grade_submit' in request.POST:
            return self.handle_grade_form(request)
        return super().post(request, *args, **kwargs)

    def handle_comment_form(self, request):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = self.object
            comment.supervisor = request.user.lecturerprofile 
            comment.save()
        return redirect('project_detail', pk=self.object.pk)

    def handle_grade_form(self, request):
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.project = self.object
            grade.supervisor = request.user.lecturerprofile 
            grade.save()
        return redirect('project_detail', pk=self.object.pk)




@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.supervisor.user != request.user:
        return HttpResponseForbidden()
    comment.delete()
    return redirect('project_detail', pk=comment.project.id)
