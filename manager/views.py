from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Task, Category, Person
from .forms import TaskForm, PersonForm

class Manager(View):
    def get(self, request):
        search_query = request.GET.get("search", "")
        if search_query:
            members = Person.objects.filter(name__icontains=search_query)
        else:
            members = Person.objects.all()
        
        tasks = Task.objects.all()
        categories = Category.objects.all()
        form = TaskForm()

        data = {
            "form": form,
            "categories": categories,
            "tasks": tasks,
            "members": members,
            "search_query": search_query
        }

        return render(request, 'manager/manager.html', data)
    
    def post(self, request):
        return self.get(request)
    
class CreatePerson(View):
    template_name = "manager/createPerson.html"
    def get(self, request):
        form = PersonForm()
        data = {
            "form": form
        }
        return render(request, self.template_name, data)
    
    def post(self, request): 
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manager:manager')
        return render(request)
