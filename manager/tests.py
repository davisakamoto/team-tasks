from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from .models import Person, Category, Task
from .forms import PersonForm, CategoryForm, TaskForm


# -------------------------------------------------
# 1. TESTES DE MODELS
# -------------------------------------------------
# Objetivo: garantir que a criação de objetos e a representação em string (__str__) funcionam.
class ModelTests(TestCase):

    def setUp(self):
        """Cria objetos base para os testes."""
        self.person1 = Person.objects.create(name="Maria Silva", role="Desenvolvedora")
        self.category1 = Category.objects.create(name="Desenvolvimento")
        self.task1 = Task.objects.create(
            title="Implementar Autenticação",
            person=self.person1,
            category=self.category1,
        )

    def test_person_model_str(self):
        """Verifica a representação em string do modelo Person."""
        self.assertEqual(str(self.person1), "Maria Silva")

    def test_category_model_str(self):
        """Verifica a representação em string do modelo Category."""
        self.assertEqual(str(self.category1), "Desenvolvimento")

    def test_task_model_str(self):
        """Verifica a representação em string do modelo Task."""
        self.assertEqual(str(self.task1), "Implementar Autenticação")

    def test_task_creation_with_relations(self):
        """Verifica se as relações ForeignKey foram salvas corretamente."""
        task = Task.objects.get(id=self.task1.id)
        self.assertEqual(task.person.name, "Maria Silva")
        self.assertEqual(task.category.name, "Desenvolvimento")


# -------------------------------------------------
# 2. TESTES DE FORMS
# -------------------------------------------------
# Objetivo: Garantir que os formulários validam os dados corretamente.
class FormTests(TestCase):

    def setUp(self):
        self.person1 = Person.objects.create(name="João Santos")
        self.category1 = Category.objects.create(name="Testes")

    def test_person_form_valid(self):
        """Testa se o PersonForm é válido com dados corretos."""
        form_data = {"name": "Novo Membro", "role": "QA"}
        form = PersonForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_person_form_invalid(self):
        """Testa se o PersonForm é inválido sem o campo 'name'."""
        form_data = {"role": "QA"}
        form = PersonForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_task_form_valid(self):
        """Testa se o TaskForm é válido com dados corretos."""
        form_data = {
            "title": "Criar testes de formulário",
            "person": self.person1.id,
            "category": self.category1.id,
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_invalid(self):
        """Testa se o TaskForm é inválido sem o campo 'title'."""
        form_data = {"person": self.person1.id}
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_category_form_valid(self):
        """Testa se o CategoryForm é válido com dados corretos."""
        form = CategoryForm(data={"name": "Nova Categoria"})
        self.assertTrue(form.is_valid())


# -------------------------------------------------
# 3. TESTES DE VIEWS
# -------------------------------------------------
# Objetivo: Simular requisições (GET, POST) e verificar se as views se comportam como esperado.
class ViewTests(TestCase):

    def setUp(self):
        """Configura dados iniciais e o cliente de teste para todas as views."""
        self.client = Client()
        self.today = timezone.now().date()

        self.person1 = Person.objects.create(name="Ana Lima", role="Frontend")
        self.person2 = Person.objects.create(name="Beto Costa", role="Backend")
        self.category_dev = Category.objects.create(name="Dev")

        self.task_pending = Task.objects.create(
            title="Tarefa Pendente",
            person=self.person1,
            category=self.category_dev,
            deadline=self.today + timedelta(days=5),
        )
        self.task_late = Task.objects.create(
            title="Tarefa Atrasada",
            person=self.person1,
            deadline=self.today - timedelta(days=2),
        )
        self.task_done = Task.objects.create(
            title="Tarefa Concluída", person=self.person2, done=True
        )

        self.manager_url = reverse("manager:manager")
        self.create_person_url = reverse("manager:createPerson")
        self.create_task_url = reverse("manager:createTask")

    def test_manager_view_get(self):
        """Testa o carregamento (GET) da página principal."""
        response = self.client.get(self.manager_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/manager.html")
        self.assertContains(response, self.task_pending.title)
        self.assertContains(response, self.task_late.title)
        self.assertContains(response, self.task_done.title)

    def test_manager_view_member_filter_not_found(self):
        """Testa o filtro de membro com um ID que não existe."""
        response = self.client.get(self.manager_url, {"member": 999})
        self.assertEqual(response.status_code, 200)

        self.assertIsNone(response.context.get("member_selected"))

    def test_edit_person_get_with_pk_zero(self):
        """Testa a lógica de 'nova pessoa' na view EditPerson com pk=0."""
        edit_url = reverse("manager:editPerson", args=[0])
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["edit"])

    def test_edit_person_post_invalid_form(self):
        """Testa o envio (POST) de dados inválidos para a edição de pessoa."""
        edit_url = reverse("manager:editPerson", args=[self.person1.id])

        response = self.client.post(edit_url, {"name": "", "role": "Incompleto"})

        self.assertEqual(response.status_code, 200)

        self.person1.refresh_from_db()
        self.assertNotEqual(self.person1.name, "")

    def test_edit_person_get_view(self):
        """Testa o carregamento (GET) da página de edição de pessoa."""
        edit_url = reverse("manager:editPerson", args=[self.person1.id])
        response = self.client.get(edit_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/person.html")

        self.assertContains(response, self.person1.name)

    def test_manager_view_search_filter(self):
        """Testa o filtro de busca de membros verificando o contexto."""
        response = self.client.get(self.manager_url, {"search": "Ana"})
        self.assertEqual(response.status_code, 200)

        members_no_contexto = response.context["members"]
        self.assertIn(self.person1, members_no_contexto)
        self.assertNotIn(self.person2, members_no_contexto)

    def test_manager_view_member_filter(self):
        """Testa o filtro de tarefas por membro."""
        response = self.client.get(self.manager_url, {"member": self.person1.id})
        self.assertContains(response, self.task_pending.title)
        self.assertNotContains(response, self.task_done.title)

    def test_manager_view_task_status_filters(self):
        """Testa todos os filtros de status das tarefas."""
        response_todo = self.client.get(self.manager_url, {"task": "todo"})
        self.assertContains(response_todo, self.task_pending.title)
        self.assertNotContains(response_todo, self.task_late.title)
        self.assertNotContains(response_todo, self.task_done.title)

        response_late = self.client.get(self.manager_url, {"task": "late"})
        self.assertNotContains(response_late, self.task_pending.title)
        self.assertContains(response_late, self.task_late.title)
        self.assertNotContains(response_late, self.task_done.title)

        response_done = self.client.get(self.manager_url, {"task": "done"})
        self.assertNotContains(response_done, self.task_pending.title)
        self.assertNotContains(response_done, self.task_late.title)
        self.assertContains(response_done, self.task_done.title)

    def test_create_person_post(self):
        """Testa a criação (POST) de uma nova pessoa."""
        person_count_before = Person.objects.count()
        response = self.client.post(
            self.create_person_url, {"name": "Carlos Dias", "role": "Designer"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.manager_url)
        self.assertEqual(Person.objects.count(), person_count_before + 1)

    def test_edit_person_post(self):
        """Testa a edição (POST) de uma pessoa."""
        edit_url = reverse("manager:editPerson", args=[self.person1.id])
        response = self.client.post(
            edit_url, {"name": "Ana Lima Editada", "role": "Frontend Sr."}
        )
        self.assertEqual(response.status_code, 302)
        self.person1.refresh_from_db()
        self.assertEqual(self.person1.name, "Ana Lima Editada")

    def test_delete_person_post(self):
        """Testa a exclusão (POST) de uma pessoa."""
        person_to_delete = Person.objects.create(name="Temporário")
        delete_url = reverse("manager:deletePerson", args=[person_to_delete.id])
        person_count_before = Person.objects.count()

        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Person.objects.count(), person_count_before - 1)

    def test_create_task_post(self):
        """Testa a criação (POST) de uma nova tarefa."""
        task_count_before = Task.objects.count()
        response = self.client.post(
            self.create_task_url,
            {
                "title": "Nova Tarefa de Teste",
                "person": self.person1.id,
                "category": self.category_dev.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), task_count_before + 1)

    def test_edit_task_post(self):
        """Testa a edição (POST) de uma tarefa."""
        edit_url = reverse("manager:editTask", args=[self.task_pending.id])
        response = self.client.post(
            edit_url,
            {
                "title": "Tarefa Pendente Editada",
                "person": self.task_pending.person.id,
                "category": self.task_pending.category.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.task_pending.refresh_from_db()
        self.assertEqual(self.task_pending.title, "Tarefa Pendente Editada")

    def test_delete_task_post(self):
        """Testa a exclusão (POST) de uma tarefa."""
        delete_url = reverse("manager:deleteTask", args=[self.task_pending.id])
        task_count_before = Task.objects.count()

        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), task_count_before - 1)

    def test_create_person_post_invalid_form(self):
        """Testa o que acontece ao submeter um formulário de pessoa inválido (sem nome)."""
        person_count_before = Person.objects.count()
        response = self.client.post(self.create_person_url, {"role": "Sem Nome"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/person.html")

        self.assertEqual(Person.objects.count(), person_count_before)

    def test_edit_person_get_with_pk_zero(self):
        """Testa o caso de borda da view EditPerson com pk=0."""

        edit_url_pk_zero = "/member/0/"
        response = self.client.get(edit_url_pk_zero)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["edit"])

    def test_toggle_done_task(self):
        """Testa a funcionalidade de marcar/desmarcar uma tarefa como concluída."""
        toggle_url = reverse("manager:toggleDone", args=[self.task_pending.id])

        self.assertFalse(self.task_pending.done)
        response = self.client.post(toggle_url, HTTP_REFERER=self.manager_url)
        self.assertEqual(response.status_code, 302)
        self.task_pending.refresh_from_db()
        self.assertTrue(self.task_pending.done)

        response = self.client.post(toggle_url)
        self.task_pending.refresh_from_db()
        self.assertFalse(self.task_pending.done)

    def test_create_task_post_invalid_form(self):
        """Testa o envio (POST) de dados inválidos para a criação de tarefa."""
        task_count_before = Task.objects.count()

        response = self.client.post(
            self.create_task_url,
            {
                "person": self.person1.id,
                "category": self.category_dev.id,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/task.html")

        self.assertEqual(Task.objects.count(), task_count_before)

    def test_edit_task_post_invalid_form(self):
        """Testa o envio (POST) de dados inválidos para a edição de tarefa."""
        edit_url = reverse("manager:editTask", args=[self.task_pending.id])
        original_title = self.task_pending.title

        response = self.client.post(
            edit_url,
            {
                "title": "", 
                "person": self.task_pending.person.id,
                "category": self.task_pending.category.id,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/task.html")

        self.task_pending.refresh_from_db()
        self.assertEqual(self.task_pending.title, original_title)
