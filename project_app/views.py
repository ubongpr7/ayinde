from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView
from django.forms import modelform_factory
from django.apps import apps

# Create your views here.

def home(request):
    
    return render(request,'index.html',)

# Generic Update View
class GenericUpdateView(UpdateView):
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
class GenericCreateView(CreateView):
    template_name = 'create.html'
    success_url = '/'

    def get_model(self):
        model_name = self.kwargs['model_name']
        app_name = self.kwargs['app_name']
        return apps.get_model(app_name, model_name)

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
        context['ajax_url'] = f'/add/{self.kwargs["app_name"]}/{self.kwargs["model_name"]}/'
        context['get_url'] = f'/list/{self.kwargs["app_name"]}/{self.kwargs["model_name"]}/'

        context['done_url'] = self.success_url
        context['model_name'] =self.kwargs['model_name']
        context['app_name'] =self.kwargs['app_name']
        return context
