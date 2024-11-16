from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from rest_framework import generics, permissions
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView

from .models import Candidat, Restaurant, Adresse, Candidature, PreferenceCandidat, PreferenceRestaurant, \
    Offre
from .serializers import (
    UserCreateSerializer,
    CandidatSerializer,
    RestaurantSerializer,
    CandidatureSerializer,
    PreferenceCandidatSerializer,
    PreferenceRestaurantSerializer,
    OffreSerializer,
    LoginSerializer,
    AdresseSerializer
)

User = get_user_model()


class AdresseListCreateView(generics.ListCreateAPIView):
    queryset = Adresse.objects.all()
    serializer_class = AdresseSerializer
    permission_classes = [permissions.AllowAny]


class UserListCreateRetrieveView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        # Si 'pk' est dans kwargs, récupérer l'utilisateur spécifique, sinon, renvoyer la liste des utilisateurs
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # Création du profil en fonction du type d'utilisateur
            if user.user_type == 'restaurant':
                Restaurant.objects.get_or_create(
                    user=user,
                    defaults={
                        'nom': user.username,
                        'tel': '0123456789',
                        'type': user.user_type
                    }
                )
            elif user.user_type == 'candidat':
                Candidat.objects.get_or_create(
                    user=user,
                    defaults={
                        'nom': user.username,
                        'tel': '0123456789',
                        'date_naissance': '2000-01-01',
                        'niveau_etude': "Niveau d'étude par défaut",
                        'experience': "Expérience par défaut",
                        'user_type': user.user_type
                    }
                )

            # Créer et retourner le token
            token, _ = Token.objects.get_or_create(user=user)

            response_data = {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'user_type': user.user_type,
                },
                'token': token.key,
                'redirect_url': '/api/users/' + str(user.id) + '/',
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vue pour récupérer les détails d'un utilisateur
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()

        # Serializer par défaut pour les informations de base de l'utilisateur
        user_data = self.get_serializer(user).data

        # Ajoutez des données spécifiques selon le type d'utilisateur
        if user.user_type == 'candidat':
            candidat = Candidat.objects.get(user=user)
            candidat_data = CandidatSerializer(candidat).data
            user_data.update(candidat_data)  # Combine les données de l'utilisateur et du candidat
        elif user.user_type == 'restaurant':
            restaurant = Restaurant.objects.get(user=user.id)
            restaurant_data = RestaurantSerializer(restaurant).data
            user_data.update(restaurant_data)  # Combine les données de l'utilisateur et du restaurant

        return Response(user_data)

    # Mise à jour des informations de l'utilisateur
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except serializers.ValidationError as e:
            print(serializer.errors)  # Affiche les erreurs de validation dans la console
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


# Vue pour récupérer les détails d'un candidat
class CandidatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        candidat = self.get_object()
        serializer = self.get_serializer(candidat)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        candidat = self.get_object()
        # Passer explicitement le contexte lors de l'initialisation du serializer
        serializer = self.get_serializer(candidat, data=request.data, partial=True, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except serializers.ValidationError as e:
            print(serializer.errors)  # Affiche les erreurs de validation dans la console
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


# Récupérer la liste des candidats si l'utilisateur est un recruteur ou administrateur
class listCandidatesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.user_type == 'recruteur' or request.user.is_staff or request.user.is_superuser:
            candidats = Candidat.objects.all()
            serializer = CandidatSerializer(candidats, many=True)
            return Response(serializer.data)
        else:
            raise PermissionDenied("Vous n'êtes pas autorisé à voir cette liste.")


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        restaurant = self.get_object()
        serializer = self.get_serializer(restaurant)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        restaurant = self.get_object()
        serializer = self.get_serializer(restaurant, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except serializers.ValidationError as e:
            print(serializer.errors)  # Affiche les erreurs de validation dans la console
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import generics, permissions
from .models import Annonce
from .serializers import AnnonceSerializer


# Vue pour gérer les annonces
class AnnonceListCreateView(generics.ListCreateAPIView):
    queryset = Annonce.objects.all()
    serializer_class = AnnonceSerializer

    # Permission pour permettre à tout le monde de voir la liste, mais seuls les utilisateurs authentifiés peuvent créer
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]  # Authentification requise pour la création
        return super().get_permissions()  # Autoriser l'accès à la liste pour tout le monde

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)  # L'utilisateur connecté qui crée l'annonce


class AnnonceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Annonce.objects.all()
    serializer_class = AnnonceSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Tous les candidats peuvent voir les annonces.
        """
        # Retourner toutes les annonces et le nom de l'utilisateur qui a créé chaque annonce
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Seuls les recruteurs ou le créateur de l'annonce peuvent modifier l'annonce.
        """
        annonce = self.get_object()
        if request.user.user_type == 'recruteur' and request.user == annonce.created_by:
            return super().put(request, *args, **kwargs)
        else:
            raise PermissionDenied("Vous n'êtes pas autorisé à modifier cette annonce.")

    def delete(self, request, *args, **kwargs):
        """
        Seuls les recruteurs ou le créateur de l'annonce peuvent supprimer l'annonce.
        """
        annonce = self.get_object()
        if request.user.user_type == 'recruteur' and request.user == annonce.created_by:
            return super().delete(request, *args, **kwargs)
        else:
            raise PermissionDenied("Vous n'êtes pas autorisé à supprimer cette annonce.")


def AnnonceView(request):
    return render(request, 'jobfiksi_api/auth/annonce.html')


# Vue pour gérer les candidatures
class CandidatureListCreateView(generics.ListCreateAPIView):
    queryset = Candidature.objects.all()
    serializer_class = CandidatureSerializer
    permission_classes = [permissions.AllowAny]


# Vue pour récupérer les préférences d'un candidat
class PreferenceCandidatDetailView(generics.RetrieveUpdateAPIView):
    queryset = PreferenceCandidat.objects.all()
    serializer_class = PreferenceCandidatSerializer
    permission_classes = [permissions.IsAuthenticated]


# Vue pour récupérer les préférences d'un restaurant
class PreferenceRestaurantDetailView(generics.RetrieveUpdateAPIView):
    queryset = PreferenceRestaurant.objects.all()
    serializer_class = PreferenceRestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]


# Vue pour gérer les offres
class OffreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offre.objects.all()
    serializer_class = OffreSerializer
    permission_classes = [permissions.IsAuthenticated]


from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    @csrf_exempt  # Désactiver la vérification CSRF pour cette méthode
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Déconnecter l'utilisateur s'il est déjà connecté
        if request.user.is_authenticated:
            logout(request)

        # Authentifier l'utilisateur
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Connecter l'utilisateur et créer la session
            login(request, user)

            # Créer une réponse de base sans token
            response_data = {
                'user': {
                    'id': user.id,  # Ajoutez d'autres champs si nécessaire, par exemple 'nom', 'prenom
                    'username': user.username,
                    'email': user.email,
                    'user_type': user.user_type,
                    'token': user.auth_token.key,
                },
            }

            # Vérifiez si le token est nécessaire et ajoutez-le si besoin
            include_token = request.data.get('include_token', False)  # optionnel dans la requête
            if include_token:
                token, _ = Token.objects.get_or_create(user=user)
                response_data['token'] = token.key

            return Response(response_data, status=status.HTTP_200_OK)

        # Journaliser l'échec d'authentification
        print(f"Authentication failed for username: {username}")
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('login')  # Redirige toujours vers la page de connexion

    @csrf_exempt
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('/login/')  # Redirige toujours vers la page de connexion
