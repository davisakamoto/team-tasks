from django.urls import path
from .views import Manager, CreatePerson

app_name = 'manager'

urlpatterns = [
    path('', Manager.as_view(), name="manager"),
    path('createPerson/', CreatePerson.as_view(), name="createPerson")
]
