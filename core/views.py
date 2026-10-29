from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .models import Board, Column, Cards
from .serializers import BoardSerializer, ColumnSerializer, CardsSerializer
from .permissions import IsBoardMemberOrReadOnly
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

def broadcast_board_update(board_id, action, data):
    """
    Sends a message to all WebSocket clients listening to this board.
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'board_{board_id}',
        {
            'type': 'board_update',
            'message': {
                'action': action,
                'data': data
            }
        }
    )

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

    def get_queryset(self):
        # Only return columns for boards owned by the logged-in user
        return Column.objects.filter(board__owner=self.request.user)


class CardViewSet(viewsets.ModelViewSet):
    queryset = Cards.objects.all()
    serializer_class = CardsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cards.objects.filter(column__board__owner=self.request.user)

    def perform_create(self, serializer):
        # Save the card to the database
        card = serializer.save()

        # Broadcast to everyone looking at this board!
        broadcast_board_update(
            board_id=card.column.board.id,
            action='card_created',
            data=(card).data
        )