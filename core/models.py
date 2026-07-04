from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return f"{self.title} - {self.description}"

class Column(models.Model):
    title = models.CharField(max_length=100)
    position = models.IntegerField(default=0)
    board = models.ForeignKey(Board, on_delete=models.CASCADE,related_name='columns')
    def __str__(self):
        return f"{self.title} - {self.position}"

class Cards(models.Model):
    title = models.CharField(max_length=100)
    position = models.IntegerField(default=0)
    column = models.ForeignKey(Column, on_delete=models.CASCADE,related_name='cards')
    def __str__(self):
        return f"{self.title} - {self.position}"