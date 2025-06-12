from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Task, Category, Person
from .forms import TaskForm, PersonForm

class Manager(View):
    def get(self, request):
        data = {}

        data['categories'] = Category.objects.all()
        data['form'] = TaskForm()

        data.update(self.get_tasks(request))
        data.update(self.get_members(request))

        return render(request, 'manager/manager.html', data)
    
    def get_tasks(self, request):
        data = {}
        today = timezone.now().date()
        
        member_id = request.GET.get("member")
        data['task_status'] = request.GET.get("task")

        if member_id:
            tasks = Task.objects.filter()
            data['member_selected'] = Person.objects.get(id=member_id)
        else:
            tasks = Task.objects.all()


        tasksTodo = tasks.filter(done=False)
        tasksLate = tasks.filter(deadline__lt=today)
        tasksDone = tasks.filter(done=True)

        data['lenAll'] = len(tasks)
        data['lenTodo'] = len(tasksTodo)
        data['lenLate'] = len(tasksLate)
        data['lenDone'] = len(tasksDone)

        if data['task_status'] == 'todo':
            tasks = tasksTodo
        elif data['task_status'] == 'late':
            tasks = tasksLate
        elif data['task_status'] == 'done':
            tasks = tasksDone

        data['tasks'] = tasks

        return data
    
    def get_members(self, request):
        search_query = request.GET.get("search", "")

        if search_query:
            members = Person.objects.filter(name__icontains=search_query)
        else:
            members = Person.objects.all()
        
        return {
            'members': members,
            'search_query': search_query
        }
    
    
class CreatePerson(View):
    template_name = "manager/person.html"
    def get(self, request):
        form = PersonForm()
        data = {
            "form": form,
            "edit": False
        }
        return render(request, self.template_name, data)
    
    def post(self, request): 
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manager:manager')
        return render(request)
    
class EditPerson(View):
    template_name = "manager/person.html"

    def get(self, request, pk):
        if pk == 0:
            form = PersonForm()
            data = {
                "form": form,
                "edit": False
            }
            return render(request, self.template_name, data)

        person = get_object_or_404(Person, pk=pk)
        form = PersonForm(instance=person)
        data = {
            "form": form,
            "edit": True,
            "person_id": person.id
        }
        return render(request, self.template_name, data)

    def post(self, request, pk):
        person = get_object_or_404(Person, pk=pk)
        form = PersonForm(request.POST, instance=person)
        data = {
            "form": form,
            "edit": True,
            "person_id": person.id
        }
        if form.is_valid():
            form.save()
            return redirect('manager:manager')
        return render(request, self.template_name, data)


class DeletePerson(View):
    def post(self, request, pk):
        person = get_object_or_404(Person, pk=pk)
        person.delete()
        return redirect('manager:manager')