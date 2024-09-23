from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OffreViewSet, CustomUserViewSet

router = DefaultRouter()
router.register(r'offres', OffreViewSet)
router.register(r'utilisateurs', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
