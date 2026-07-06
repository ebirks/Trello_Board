from django.urls import path, include
from rest_framework import routers
from .views import BoardViewSet, ColumnViewSet, CardsViewSet

router = routers.DefaultRouter()
router.register(r'boards', BoardViewSet)
router.register(r'columns', ColumnViewSet)
router.register(r'cards', CardsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]