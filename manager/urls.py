from django.urls import path
from .views import Manager

urlpatterns = [
    path('', Manager.as_view(), name="manager")
]
