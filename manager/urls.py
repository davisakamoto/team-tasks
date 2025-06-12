from django.urls import path
from .views import Manager, CreatePerson, EditPerson, DeletePerson

app_name = 'manager'

urlpatterns = [
    path('', Manager.as_view(), name="manager"),
    path('member/new', CreatePerson.as_view(), name="createPerson"),
    path('member/<int:pk>/', EditPerson.as_view(), name="editPerson"),
    path('member/<int:pk>/delete', DeletePerson.as_view(), name="deletePerson")
]
