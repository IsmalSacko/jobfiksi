from django.urls import path

from .views import (
    RestaurantProfileView,
    AnnonceListCreateView,
    CandidatureListCreateView,
    UserDetailView,
    ListCandidatesView,
    AnnonceDetailView,
    CandidatProfileView,
    CandidatDetailView, UserListCreateRetrieveView, CandidatureDetailView, RestaurantListView, StartConversationView,
    ContractListCreateView, RestaurantDetailView, ConversationMessageView

)

urlpatterns = [
    # Route pour créer un utilisateur (candidat ou restaurant)
    path('users/', UserListCreateRetrieveView.as_view(), name='user_create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),

    # Route pour lister les candidats
    path('candidats/', ListCandidatesView.as_view(), name='candidat-list'),
    path('candidats/<int:pk>/', CandidatDetailView.as_view(), name='candidat-detail'),
    # Route pour lister les restaurants
    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurants/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
    # Routes pour les restaurants
    path('restaurants/profile/', RestaurantProfileView.as_view(), name='restaurant-profile'),

    path('candidats/profile/', CandidatProfileView.as_view(), name='candidat-profile'),
    # Routes pour gérer les annonces
    path('annonces/', AnnonceListCreateView.as_view(), name='annonce_create'),
    path('annonces/<int:pk>/', AnnonceDetailView.as_view(), name='annonce-detail'),

    # Routes pour gérer les candidatures
    path('candidatures/', CandidatureListCreateView.as_view(), name='candidature-list-create'),
    path('candidatures/<int:pk>/', CandidatureDetailView.as_view(), name='candidature-detail'),

    path('contracts/', ContractListCreateView.as_view(), name='contracts'),

    # Créer une conversation
    path('conversations/start/', StartConversationView.as_view(), name='start-conversation'),

    # Lister et envoyer des messages dans une conversation
    path('conversations/<int:conversation_id>/messages/', ConversationMessageView.as_view(),
         name='conversation-messages'),
]
