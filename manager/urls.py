from django.urls import path
from .views import Manager, CreatePerson, EditPerson, DeletePerson

app_name = 'manager'

urlpatterns = [
    path('', Manager.as_view(), name="manager"),
    path('createPerson/', CreatePerson.as_view(), name="createPerson"),
    path('editPerson/<int:pk>/', EditPerson.as_view(), name="editPerson"),
    path('deletePerson/<int:pk>/', DeletePerson.as_view(), name="deletePerson")
]
