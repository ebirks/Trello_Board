from django.urls import path, include
from rest_framework import routers
from .views import BoardViewSet, ColumnViewSet, CardViewSet

router = routers.DefaultRouter()
router.register(r'boards', BoardViewSet)
router.register(r'columns', ColumnViewSet)
router.register(r'cards', CardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]