from django.urls import path
from .views import (
    RestaurantProfileView,
    AnnonceListCreateView,
    CandidatureListCreateView,
    PreferenceCandidatDetailView,
    PreferenceRestaurantDetailView,
    OffreDetailView,
    UserListCreateRetrieveView,
    AdresseListCreateView,
    UserDetailView,
    listCandidatesView, AnnonceDetailView, CandidatProfileView

)

urlpatterns = [
    # Route pour créer un utilisateur (candidat ou restaurant)
    path('users/', UserListCreateRetrieveView.as_view(), name='user_create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),

    # Route pour lister les candidats
    path('candidats/', listCandidatesView.as_view(), name='candidat-list'),
    # Routes pour les restaurants
    path('restaurants/profile/', RestaurantProfileView.as_view(), name='restaurant-profile'),
    path('candidats/profile/', CandidatProfileView.as_view(), name='candidat-profile'),
    # Routes pour gérer les annonces
    path('annonces/', AnnonceListCreateView.as_view(), name='annonce_create'),
    path('annonces/<int:pk>/', AnnonceDetailView.as_view(), name='annonce-detail'),

    # Routes pour gérer les candidatures
    path('candidatures/', CandidatureListCreateView.as_view(), name='candidature-list-create'),

    # Routes pour récupérer et mettre à jour les préférences d'un candidat
    path('candidats/preferences/<int:pk>/', PreferenceCandidatDetailView.as_view(), name='preference-candidat-detail'),

    # Routes pour récupérer et mettre à jour les préférences d'un restaurant
    path('restaurants/preferences/<int:pk>/', PreferenceRestaurantDetailView.as_view(),
         name='preference-restaurant-detail'),


    path('adresse/', AdresseListCreateView.as_view(), name='adresse-create'),

]
