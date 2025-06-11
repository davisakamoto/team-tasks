from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    done = models.BooleanField(default=False)
    deadline = models.DateField(null=True, blank=True)
    doneAt = models.DateTimeField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Person(models.Model):
    name = models.CharField(max_length=200) 
    email = models.CharField(blank=True, null=True)
    role = models.CharField(blank=True, null=True)
    joinedAt = models.DateField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title