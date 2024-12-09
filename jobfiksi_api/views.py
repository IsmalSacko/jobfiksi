from email.utils import unquote

import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import Restaurant, Candidature, Annonce
from .serializers import (
    UserCreateSerializer,
    RestaurantSerializer,
    CandidatureSerializer,
    LoginSerializer, AnnonceSerializer,

)

User = get_user_model()


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
            user.is_active = True  # Activer immédiatement l'utilisateur
            user.save()

            # Création automatique du token pour l'utilisateur
            token, created = Token.objects.get_or_create(user=user)

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
                        'niveau_etude': "BAC+5",
                        'experience': "Expérience par défaut",
                        'user_type': user.user_type
                    }
                )

            # Générer dynamiquement le lien vers la page de connexion
            login_url = request.build_absolute_uri(reverse('login'))

            # Envoyer un email de confirmation
            send_mail(
                subject="Bienvenue sur JobFiksi - Inscription réussie",
                message=(
                    f"Bonjour {user.username},\n\n"
                    f"Votre inscription a bien été prise en compte.\n\n"
                    f"Vous pouvez maintenant vous connecter via ce lien : {login_url}\n\n"
                    f"Cordialement,\nL'équipe JobFiksi"
                ),
                from_email="jobfiksi@gmail.com",
                recipient_list=[user.email],
                fail_silently=False,
            )

            # Retourner une réponse claire avec le token
            response_data = {
                'message': 'Inscription réussie ! Un email de confirmation a été envoyé.',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'user_type': user.user_type,
                },
                'token': token.key
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
        user = self.get_object()  # Récupérer l'objet utilisateur actuel
        user_serializer = self.get_serializer(user, data=request.data, partial=True)

        # Valider et enregistrer les modifications de l'utilisateur
        try:
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()  # Enregistrer les modifications de l'utilisateur
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        # Si l'utilisateur est un candidat, mettre à jour les informations du candidat
        if user.user_type == 'candidat':
            try:
                candidat = Candidat.objects.get(user=user)  # Récupérer l'objet Candidat associé
                candidat_serializer = CandidatSerializer(candidat, data=request.data, partial=True)
                if candidat_serializer.is_valid():
                    candidat_serializer.save()  # Enregistrer les modifications du candidat
                else:
                    return Response(candidat_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Candidat.DoesNotExist:
                return Response({'detail': 'Candidat not found for this user.'}, status=status.HTTP_404_NOT_FOUND)

        # Si l'utilisateur est un restaurant, mettre à jour les informations du restaurant
        elif user.user_type == 'restaurant':
            try:
                restaurant = Restaurant.objects.get(user=user.id)  # Récupérer l'objet Restaurant associé
                restaurant_serializer = RestaurantSerializer(restaurant, data=request.data, partial=True)
                if restaurant_serializer.is_valid():
                    restaurant_serializer.save()  # Enregistrer les modifications du restaurant
                else:
                    return Response(restaurant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Restaurant.DoesNotExist:
                return Response({'detail': 'Restaurant not found for this user.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(user_serializer.data)  # Retourner les données de l'utilisateur, incluant les mises à jour


# Récupérer la liste des candidats si l'utilisateur est un recruteur ou administrateur
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from .models import Candidat
from .serializers import CandidatSerializer


class ListCandidatesView(generics.ListAPIView):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer
    permission_classes = [permissions.IsAuthenticated]  # Authentification requise

    def get_queryset(self):
        queryset = Candidat.objects.all()
        search_query = self.request.query_params.get('search', None)

        if search_query:
            decoded_search_query = unquote(search_query)

            # Construire une condition Q dynamique pour tous les champs pertinents
            search_filter = Q()
            fields_to_search = [
                'nom', 'prenom', 'tel', 'niveau_etude', 'disponibilite', 'experience',
                'etablissement', 'formation', 'ville', 'pays', 'plage_horaire',
                'disponibilite', 'preference_salaire', 'salaire_min', 'salaire_max',
                'genre', 'type_de_poste_recherche', 'type_de_contrat_recherche',
                'langues_parlees', 'iban', 'secu_sociale', 'code_postal'
            ]

            for field in fields_to_search:
                search_filter |= Q(**{f"{field}__icontains": decoded_search_query})

            # Ajouter le filtre à la requête
            queryset = queryset.filter(search_filter)

        return queryset


class CandidatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer
    permission_classes = [permissions.IsAuthenticated]  # Authentification requise

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]  # Authentification requise pour PUT, PATCH, DELETE
        return super().get_permissions()  #


def get_lyon_coordinates():
    """Obtenir les coordonnées de Lyon via Nominatim (OpenStreetMap)."""
    try:
        response = requests.get(
            'https://nominatim.openstreetmap.org/search',
            params={
                'q': 'Lyon, France',  # Recherche pour Lyon
                'format': 'json',
                'limit': 5
            }
        )

        if response.status_code == 200 and response.json():
            location_data = response.json()[0]
            return float(location_data['lat']), float(location_data['lon'])
    except Exception as e:
        print(f"Erreur lors de l'appel à Nominatim : {e}")

    # Coordonnées par défaut pour Lyon
    return 45.764043, 4.835659


from urllib.parse import unquote
from django.db.models import Q
from geopy.distance import geodesic

# Coordonnées de Lyon (par défaut)
LYON_COORDINATES = (45.764043, 4.835659)


class AnnonceListCreateView(generics.ListCreateAPIView):
    serializer_class = AnnonceSerializer

    # Permission pour permettre à tout le monde de voir la liste, mais seuls les utilisateurs authentifiés peuvent créer
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]  # Authentification requise pour la création
        return super().get_permissions()  # Autoriser l'accès à la liste pour tout le monde

    def get_queryset(self):
        queryset = Annonce.objects.all()

        # Filtrage par mot-clé (si un mot-clé est fourni)
        search_query = self.request.query_params.get('search', None)
        if search_query:
            decoded_search_query = unquote(search_query)

            # Appliquer la recherche sur plusieurs champs
            queryset = queryset.filter(
                Q(titre__icontains=decoded_search_query) |  # Recherche par titre
                Q(description__icontains=decoded_search_query) |  # Recherche par description
                Q(type_contrat__icontains=decoded_search_query) |  # Recherche par type de contrat
                Q(type_annonce__icontains=decoded_search_query) |  # Recherche par type d'annonce
                Q(temps_travail__icontains=decoded_search_query) |  # Recherche par temps de travail
                Q(statut__icontains=decoded_search_query) |  # Recherche par statut
                Q(avantages__icontains=decoded_search_query) |  # Recherche par avantages
                Q(mode_paiement__icontains=decoded_search_query) |  # Recherche par mode de paiement
                Q(created_by__username__icontains=decoded_search_query) |  # Recherche par créateur
                Q(salaire__icontains=decoded_search_query) |  # Recherche par salaire
                Q(nb_heures_semaine__icontains=decoded_search_query) |  # Recherche par nombre d'heures
                Q(created_by__in=User.objects.filter(username__icontains=decoded_search_query))
                # Recherche par créateur
            )

        # Récupérer la position de l'utilisateur (ou utiliser Lyon par défaut)
        user_latitude = self.request.query_params.get('latitude', None)
        user_longitude = self.request.query_params.get('longitude', None)

        # Si l'utilisateur n'a pas fourni de coordonnées, utiliser Lyon
        if not user_latitude or not user_longitude:
            user_latitude, user_longitude = LYON_COORDINATES

        radius = self.request.query_params.get('radius', 25)  # Rayon par défaut de 25 km

        user_latitude = float(user_latitude)
        user_longitude = float(user_longitude)
        radius = float(radius)

        # Filtrer les annonces avec des coordonnées valides
        valid_annonces = queryset.filter(latitude__isnull=False, longitude__isnull=False)

        # Ajouter la distance et filtrer selon le rayon
        annonces_with_distance = []
        for annonce in valid_annonces:
            # Calculer la distance entre l'utilisateur et l'offre
            distance = geodesic(
                (user_latitude, user_longitude),
                (annonce.latitude, annonce.longitude)
            ).km
            annonce.distance = distance  # Ajouter la distance calculée à l'offre

            # Filtrer les annonces selon le rayon
            if distance <= radius:
                annonces_with_distance.append(annonce)

        # Passer les coordonnées utilisateur au sérialiseur via le contexte
        context = {
            'user_latitude': user_latitude,
            'user_longitude': user_longitude
        }

        # Sérialiser les annonces avec le contexte
        serializer = AnnonceSerializer(annonces_with_distance, many=True, context=context)
        return serializer.data

    def perform_create(self, serializer):
        # Si aucune latitude/longitude n'est fournie, utiliser les coordonnées par défaut (Lyon)
        latitude = self.request.data.get('latitude', None)
        longitude = self.request.data.get('longitude', None)

        if not latitude or not longitude:
            latitude, longitude = LYON_COORDINATES

        serializer.save(
            created_by=self.request.user,
            latitude=latitude,
            longitude=longitude
        )


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


class CandidatureListCreateView(generics.ListCreateAPIView):
    serializer_class = CandidatureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtrer les candidatures pour le candidat connecté
        user = self.request.user
        if user.user_type == 'candidat':
            return Candidature.objects.filter(candidat__user=user)
        return Candidature.objects.none()

    def perform_create(self, serializer):
        # Récupérer l'annonce associée à la candidature
        annonce_id = self.request.data.get('annonce')
        if not annonce_id:
            raise serializers.ValidationError("L'annonce est obligatoire.")

        try:
            annonce = Annonce.objects.get(id=annonce_id)
        except Annonce.DoesNotExist:
            raise serializers.ValidationError("L'annonce spécifiée n'existe pas.")

        # Vérifier si le candidat est connecté
        try:
            candidat = Candidat.objects.get(user=self.request.user)
        except Candidat.DoesNotExist:
            raise ValidationError("Vous n'êtes pas autorisé à postuler à une annonce.")

        # Vérifier si le candidat a déjà postulé à cette annonce
        candidature_exists = Candidature.objects.filter(candidat=candidat, annonce=annonce).exists()
        if candidature_exists:
            raise serializers.ValidationError("Vous avez déjà postulé à cette annonce.")

        # Créer la candidature
        serializer.save(candidat=candidat, annonce=annonce)


# Vue pour gérer les détails d'une candidature
class CandidatureDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CandidatureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtrer les candidatures pour le candidat connecté
        user = self.request.user
        if user.user_type == 'candidat':
            return Candidature.objects.filter(candidat__user=user)
        return Candidature.objects.none()

    def perform_update(self, serializer):
        # Vérifier que l'utilisateur est le créateur de la candidature
        candidature = self.get_object()
        if self.request.user != candidature.candidat.user:
            raise PermissionDenied("Vous n'êtes pas autorisé à modifier cette candidature.")
        serializer.save()

    def perform_destroy(self, instance):
        # Vérifier que l'utilisateur est le créateur de la candidature
        if self.request.user != instance.candidat.user:
            raise PermissionDenied("Vous n'êtes pas autorisé à supprimer cette candidature.")
        instance.delete()


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


class CandidatProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CandidatSerializer
    permission_classes = [IsAuthenticated]  # Seul un utilisateur authentifié peut accéder à cette vue

    def get_object(self):
        # On récupère l'utilisateur connecté
        user = self.request.user
        candidt = Candidat.objects.get(user_id=user.id)
        # Puis on cherche le profil Candidat lié à cet utilisateur
        return candidt

    def perform_update(self, serializer):
        # Cette méthode est appelée après validation des données.
        # Elle met à jour le profil du candidat
        candidat = self.get_object()
        serializer.save(candidat=candidat)


class RestaurantProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]  # Seul un utilisateur authentifié peut accéder à cette vue

    def get_object(self):
        # On récupère l'utilisateur connecté
        user = self.request.user
        # Puis on cherche le profil Restaurant lié à cet utilisateur
        return Restaurant.objects.get(user_id=user.id)

    def perform_update(self, serializer):
        # Cette méthode est appelée après validation des données.
        # Elle met à jour le profil du restaurant
        restaurant = self.get_object()
        serializer.save(restaurant=restaurant)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
        })


# retrouver tous les restaurants
class RestaurantListView(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
