from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .models import Board, Column, Cards
from .serializers import BoardSerializer, ColumnSerializer, CardsSerializer
from .permissions import IsBoardMemberOrReadOnly  # <-- MUST BE HERE


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsBoardMemberOrReadOnly]  # <-- MUST BE HERE

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Board.objects.filter(
            models.Q(owner=self.request.user) |
            models.Q(memberships__user=self.request.user)
        ).distinct()

class ColumnViewSet(viewsets.ModelViewSet):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer
    permission_classes = [IsAuthenticated]

class CardsViewSet(viewsets.ModelViewSet):
    queryset = Cards.objects.all()
    serializer_class = CardsSerializer
    permission_classes = [IsAuthenticated]