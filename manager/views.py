from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse

from .models import Task, Category
from .forms import TaskForm

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