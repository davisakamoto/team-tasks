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

        # Filtro por membro, se um for selecionado
        if member_id and member_id.isdigit():
            tasks = Task.objects.filter(person_id=member_id)
            try:
                data['member_selected'] = Person.objects.get(id=member_id)
            except Person.DoesNotExist:
                tasks = Task.objects.all()
                data['member_selected'] = None
        else:
            tasks = Task.objects.all()
            data['member_selected'] = None

        # Filtros por status e métricas
        tasksTodo = tasks.filter(done=False, deadline__gte=today)
        tasksLate = tasks.filter(done=False, deadline__lt=today)
        tasksDone = tasks.filter(done=True)

        data['lenAll'] = tasks.count()
        data['lenTodo'] = tasksTodo.count()
        data['lenLate'] = tasksLate.count()
        data['lenDone'] = tasksDone.count()

        # Decidindo qual filtro de status utilizar
        if data['task_status'] == 'todo':
            tasks_to_display = tasksTodo
        elif data['task_status'] == 'late':
            tasks_to_display = tasksLate
        elif data['task_status'] == 'done':
            tasks_to_display = tasksDone
        else:
            tasks_to_display = tasks

        data['tasks'] = tasks_to_display.order_by('-deadline')
        data['today'] = today 

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

class ToggleDoneTask(View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.done = not task.done # Inverte o valor booleano
        task.save()
        
        # Redireciona de volta para a URL de onde o usuário veio
        return redirect(request.META.get('HTTP_REFERER', 'manager:manager'))


class EditTask(View):
    template_name = "manager/task.html" # Certifique-se que o template está correto

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(instance=task)
        data = {
            "form": form,
            "edit": True,
            "task_id": task.id
        }
        return render(request, self.template_name, data)

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('manager:manager')
        
        # Se o formulário não for válido, renderiza a página novamente com os erros
        data = {
            "form": form,
            "edit": True,
            "task_id": task.id
        }
        return render(request, self.template_name, data)
 
class CreateTask(View):
    template_name = "manager/task.html"

    def get(self, request):
        form = TaskForm()
        data = {
            "form": form,
            "edit": False
        }
        return render(request, self.template_name, data)
    
    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manager:manager')
        return render(request)

class DeleteTask(View):
    def post(self, request, pk):
        person = get_object_or_404(Task, pk=pk)
        person.delete()
        return redirect('manager:manager')