from django.contrib import admin
from .models import Board,Column,Cards, BoardMembership

# Register your models here.
admin.site.register(Board)
admin.site.register(Column)
admin.site.register(Cards)
admin.site.register(BoardMembership)