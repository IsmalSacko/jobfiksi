from django.urls import path
from .views import (
    CustomUserListCreateView,
    CustomUserDetailView,
    OffreListCreateView,
    OffreDetailView,
    RecruiterListCreateView,
    RecruiterDetailView,
    CandidateListCreateView,
    CandidateDetailView,
    LoginView,


)

urlpatterns = [
    path('users/', CustomUserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'),
    path('offres/', OffreListCreateView.as_view(), name='offre-list-create'),
    path('offres/<int:pk>/', OffreDetailView.as_view(), name='offre-detail'),
        # URLs pour les recruteurs
    path('recruteurs/', RecruiterListCreateView.as_view(), name='recruiter-list'),
    path('recruteurs/<int:pk>/', RecruiterDetailView.as_view(), name='recruiter-detail'),
    
    # URLs pour les candidats
    path('candidats/', CandidateListCreateView.as_view(), name='candidate-list'),
    path('candidats/<int:pk>/', CandidateDetailView.as_view(), name='candidate-detail'),

     path('login/', LoginView.as_view(), name='login'),

   
]

