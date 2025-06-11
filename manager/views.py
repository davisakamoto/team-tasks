from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse

from .models import Task, Category, Person
from .forms import TaskForm, PersonForm

class Manager(View):
    def get(self, request):
        tasks = Task.objects.all()
        categories = Category.objects.all()

        form = TaskForm()

        data = {
            "form": form,
            "categories": categories,
            "tasks": tasks,
            "members": [
                {
                    "name": "Arthur Carvalho",
                    "role": "Desenvolvedor Front-End",
                    "picture": None
                },
                {
                    "name": "Davi Carvalho",
                    "role": "Desenvolvedor Back-End",
                    "picture": None
                },
                {
                    "name": "Davi Sakamoto",
                    "role": "Tech Lead",
                    "picture": None
                }
            ]
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
    
