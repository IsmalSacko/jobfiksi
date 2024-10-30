from django.urls import path
from .views import (
    CandidatDetailView,
    RestaurantDetailView,
    AnnonceListCreateView,
    CandidatureListCreateView,
    PreferenceCandidatDetailView,
    PreferenceRestaurantDetailView,
    OffreDetailView,
    UserListCreateRetrieveView,
    AdresseListCreateView,
    UserDetailView,
   listCandidatesView

   
    
)


urlpatterns = [
    # Route pour créer un utilisateur (candidat ou restaurant)
    path('users/', UserListCreateRetrieveView.as_view(), name='user_create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),

    path('candidats/', listCandidatesView.as_view(), name='candidat-list'),
    # Routes pour un candidat
    path('candidats/<int:pk>/', CandidatDetailView.as_view(), name='candidat-detail'),

    # Routes pour les restaurants
    path('restaurants/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),

    # Routes pour gérer les annonces
    path('annonces/', AnnonceListCreateView.as_view(), name='annonce_create'),
    path('annonces/<int:pk>/', AnnonceListCreateView.as_view(), name='annonce-detail'),
    

    # Routes pour gérer les candidatures
    path('candidatures/', CandidatureListCreateView.as_view(), name='candidature-list-create'),

    # Routes pour récupérer et mettre à jour les préférences d'un candidat
    path('candidats/preferences/<int:pk>/', PreferenceCandidatDetailView.as_view(), name='preference-candidat-detail'),

    # Routes pour récupérer et mettre à jour les préférences d'un restaurant
    path('restaurants/preferences/<int:pk>/', PreferenceRestaurantDetailView.as_view(), name='preference-restaurant-detail'),

    # Routes pour gérer les offres
    path('offres/<int:pk>/', OffreDetailView.as_view(), name='offre-detail'),
    #  Route pour les villes
    path('adresse/', AdresseListCreateView.as_view(), name='adresse-create'),
    

]
