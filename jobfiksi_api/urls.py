from django.urls import path
from .views import (
    CustomUserListCreateView,
    CustomUserDetailView,
    OffreListCreateView,
    OffreDetailView
)

urlpatterns = [
    path('users/', CustomUserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'),
    path('offres/', OffreListCreateView.as_view(), name='offre-list-create'),
    path('offres/<int:pk>/', OffreDetailView.as_view(), name='offre-detail'),
]

