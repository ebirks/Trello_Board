from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards', null=True)
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

class BoardMembership(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer'),
    ]

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='board_memberships')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='viewer')

    class Meta:
        unique_together = ('board', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.board.title} - {self.role}"
