from django.urls import path
from . import views

app_name = 'manager'

urlpatterns = [
    path('', views.Manager.as_view(), name="manager"),
    path('member/new', views.CreatePerson.as_view(), name="createPerson"),
    path('member/<int:pk>/', views.EditPerson.as_view(), name="editPerson"),
    path('member/<int:pk>/delete', views.DeletePerson.as_view(), name="deletePerson"),
    path('task/new', views.CreateTask.as_view(), name="createTask"),
    path('task/<int:pk>/', views.EditTask.as_view(), name="editTask"),
    path('task/<int:pk>/delete', views.DeleteTask.as_view(), name="deleteTask"),
    path('task/<int:pk>/toggle-done/', views.ToggleDoneTask.as_view(), name="toggleDone")
]
