from email.utils import unquote

import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Restaurant, Candidature, Annonce, Candidat, Conversation, Message, Contract
from .serializers import (
    UserCreateSerializer,
    RestaurantSerializer,
    CandidatureSerializer,
    LoginSerializer,
    AnnonceSerializer,
    CandidatSerializer,
    ConversationSerializer,
    MessageSerializer, ContractSerializer,
)

User = get_user_model()

# Coordonnées de Lyon (par défaut)
LYON_COORDINATES = (45.764043, 4.835659)


class UserListCreateRetrieveView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
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
            # login_url = request.build_absolute_uri(reverse('login'))

            # # Envoyer un email de confirmation
            # send_mail(
            #     subject="Bienvenue sur JobFiksi - Inscription réussie",
            #     message=(
            #         f"Bonjour {user.username},\n\n"
            #         f"Votre inscription a bien été prise en compte.\n\n"
            #         f"Vous pouvez maintenant vous connecter via ce lien : {login_url}\n\n"
            #         f"Cordialement,\nL'équipe JobFiksi"
            #     ),
            #     from_email="jobfiksi@gmail.com",
            #     recipient_list=[user.email],
            #     fail_silently=False,
            # )

            # Retourner une réponse claire avec le token
            response_data = {
                'message': 'Inscription réussie !',
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


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        user_data = self.get_serializer(user).data

        if user.user_type == 'candidat':
            candidat = Candidat.objects.get(user=user)
            candidat_data = CandidatSerializer(candidat).data
            user_data.update(candidat_data)
        elif user.user_type == 'restaurant':
            restaurant = Restaurant.objects.get(user=user.id)
            restaurant_data = RestaurantSerializer(restaurant).data
            user_data.update(restaurant_data)

        return Response(user_data)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user_serializer = self.get_serializer(user, data=request.data, partial=True)

        try:
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        if user.user_type == 'candidat':
            try:
                candidat = Candidat.objects.get(user=user)
                candidat_serializer = CandidatSerializer(candidat, data=request.data, partial=True)
                if candidat_serializer.is_valid():
                    candidat_serializer.save()
                else:
                    return Response(candidat_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Candidat.DoesNotExist:
                return Response({'detail': 'Candidat not found for this user.'}, status=status.HTTP_404_NOT_FOUND)

        elif user.user_type == 'restaurant':
            try:
                restaurant = Restaurant.objects.get(user=user.id)
                restaurant_serializer = RestaurantSerializer(restaurant, data=request.data, partial=True)
                if restaurant_serializer.is_valid():
                    restaurant_serializer.save()
                else:
                    return Response(restaurant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Restaurant.DoesNotExist:
                return Response({'detail': 'Restaurant not found for this user.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(user_serializer.data)


class ListCandidatesView(generics.ListAPIView):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Candidat.objects.all()
        search_query = self.request.query_params.get('search', None)

        if search_query:
            decoded_search_query = unquote(search_query)
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

            queryset = queryset.filter(search_filter)

        return queryset


class CandidatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()


def get_lyon_coordinates():
    """Obtenir les coordonnées de Lyon via Nominatim (OpenStreetMap)."""
    try:
        response = requests.get(
            'https://nominatim.openstreetmap.org/search',
            params={
                'q': 'Lyon, France',
                'format': 'json',
                'limit': 5
            }
        )

        if response.status_code == 200 and response.json():
            location_data = response.json()[0]
            return float(location_data['lat']), float(location_data['lon'])
    except Exception as e:
        print(f"Erreur lors de l'appel à Nominatim : {e}")

    return 45.764043, 4.835659


class AnnonceListCreateView(generics.ListCreateAPIView):
    serializer_class = AnnonceSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]  # Authentification requise pour la création
        return super().get_permissions()  # Autoriser l'accès à la liste pour tout le monde

    def get_queryset(self):

        # Récupérer les paramètres de recherche depuis l'URL
        queryset = Annonce.objects.all()
        search_query = self.request.query_params.get('search', None)
        titre_query = self.request.query_params.get('titre', None)
        ville_query = self.request.query_params.get('ville', None)
        nom_query = self.request.query_params.get('nom', None)

        # Filtrer selon les critères envoyés
        if search_query:
            decoded_search_query = unquote(search_query)  # Décoder la requête
            queryset = queryset.filter(
                Q(titre__icontains=decoded_search_query) |
                Q(description__icontains=decoded_search_query)
            )

        if titre_query:
            decoded_titre_query = unquote(titre_query)
            queryset = queryset.filter(titre__icontains=decoded_titre_query)  # Recherche par titre

        if ville_query:
            decoded_ville_query = unquote(ville_query)
            queryset = queryset.filter(ville__icontains=decoded_ville_query)  # Recherche par ville

        if nom_query:
            decoded_nom_query = unquote(nom_query)
            queryset = queryset.filter(
                created_by__username__icontains=decoded_nom_query)  # Recherche par nom (utilisateur créateur)
        # Si aucun résultat n'est trouvé, retourner les plus récentes annonces
        if not queryset.exists():
            queryset = Annonce.objects.all().order_by('-created_at')  # Retourner les annonces les plus récentes

        # Trier les résultats
        queryset = queryset.order_by('-created_at')
        return queryset

    def perform_create(self, serializer):
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
    """
    Vue pour récupérer, modifier ou supprimer une annonce
    uniquement si l'utilisateur est le créateur et de type restaurant.
    """
    queryset = Annonce.objects.all()
    serializer_class = AnnonceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        annonce = self.get_object()

        # Vérifier si l'utilisateur est le créateur et de type 'restaurant'
        if request.user == annonce.created_by and request.user.user_type == 'restaurant':
            return super().put(request, *args, **kwargs)

        # Sinon, lever une exception
        raise PermissionDenied("Vous n'êtes pas autorisé à modifier cette annonce.")

    def delete(self, request, *args, **kwargs):
        annonce = self.get_object()

        # Vérifier si l'utilisateur est le créateur et de type 'restaurant'
        if request.user == annonce.created_by and request.user.user_type == 'restaurant':
            return super().delete(request, *args, **kwargs)

        # Sinon, lever une exception
        raise PermissionDenied("Vous n'êtes pas autorisé à supprimer cette annonce.")


class CandidatureListCreateView(generics.ListCreateAPIView):
    """
    Vue pour lister les candidatures d'un utilisateur de type candidat
    et afficher les annonces disponibles pour une nouvelle candidature.
    """
    serializer_class = CandidatureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Filtrer uniquement les candidatures du candidat connecté
        if user.user_type == 'candidat':
            return Candidature.objects.filter(candidat__user=user)
        return Candidature.objects.none()

    def list(self, request, *args, **kwargs):
        """
        Retourne les candidatures existantes et la liste des annonces disponibles.
        """
        # Liste des candidatures du candidat connecté
        candidatures = self.get_queryset()
        candidature_serializer = self.get_serializer(candidatures, many=True)

        # Liste des annonces disponibles
        annonces = Annonce.objects.all()
        annonce_serializer = AnnonceSerializer(annonces, many=True)

        # Combiner les deux dans une réponse
        return Response({
            "candidatures": candidature_serializer.data,
            "annonces": annonce_serializer.data,
        })

    def perform_create(self, serializer):
        # Récupérer l'annonce pour la candidature
        annonce_id = self.request.data.get('annonce')
        if not annonce_id:
            raise serializers.ValidationError({"annonce": "L'annonce est obligatoire."})

        # Vérification si l'annonce existe
        try:
            annonce = Annonce.objects.get(id=annonce_id)
        except Annonce.DoesNotExist:
            raise serializers.ValidationError({"annonce": "L'annonce spécifiée n'existe pas."})

        # Vérifier si l'utilisateur connecté est un candidat
        try:
            candidat = Candidat.objects.get(user=self.request.user)
        except Candidat.DoesNotExist:
            raise serializers.ValidationError({"candidat": "Vous n'êtes pas autorisé à postuler à une annonce."})

        # Vérifier si une candidature existe déjà pour cette annonce
        candidature_exists = Candidature.objects.filter(candidat=candidat, annonce=annonce).exists()
        if candidature_exists:
            raise serializers.ValidationError({"candidature": "Vous avez déjà postulé à cette annonce."})

        # Enregistrer la candidature
        serializer.save(candidat=candidat, annonce=annonce)


class CandidatureDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CandidatureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'candidat':
            return Candidature.objects.filter(candidat__user=user)
        return Candidature.objects.none()

    def perform_update(self, serializer):
        candidature = self.get_object()
        if self.request.user != candidature.candidat.user:
            raise PermissionDenied("Vous n'êtes pas autorisé à modifier cette candidature.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.candidat.user:
            raise PermissionDenied("Vous n'êtes pas autorisé à supprimer cette candidature.")
        instance.delete()


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    @csrf_exempt
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if request.user.is_authenticated:
            logout(request)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            response_data = {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'user_type': user.user_type,
                    'token': user.auth_token.key,
                },
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('login')

    @csrf_exempt
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('/login/')


class CandidatProfileView(generics.RetrieveUpdateAPIView):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Récupérer le profil lié à l'utilisateur connecté
        return Candidat.objects.get(user=self.request.user)


class RestaurantProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return Restaurant.objects.get(user_id=user.id)

    def perform_update(self, serializer):
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


class RestaurantListView(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue pour récupérer, mettre à jour ou supprimer un restaurant spécifique.
    """
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Restaurant.objects.all()


class StartConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        candidat = request.data.get('candidat')  # ID du candidat
        restaurant = request.user.restaurant_profile  # Récupérer le restaurant connecté

        # Créer une conversation entre le candidat et le restaurant
        conversation = Conversation.objects.create(
            candidat=candidat,
            restaurant=restaurant
        )

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)


class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        conversation_id = request.data.get('conversation_id')
        contenu = request.data.get('contenu')
        type_message = request.data.get('type_message')  # 'text' ou 'file'

        # Vérifier si la conversation existe
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"detail": "Conversation not found"}, status=404)

        # Créer un message
        message = Message.objects.create(
            conversation=conversation,
            auteur=request.user,
            contenu=contenu,
            type_message=type_message
        )

        serializer = MessageSerializer(message)
        return Response(serializer.data)

    class ContractCreateView(generics.CreateAPIView):
        queryset = Contract.objects.all()
        serializer_class = ContractSerializer
        permission_classes = [IsAuthenticated]  # Assurez-vous que l'utilisateur est authentifié


class ContractListCreateView(generics.ListCreateAPIView):
    """
        Vue pour lister et créer des contrats.
        """
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Si l'utilisateur est un restaurant, afficher ses contrats
        if hasattr(user, 'restaurant'):
            return Contract.objects.filter(restaurant=user.restaurant)
        # Si l'utilisateur est un candidat, afficher ses contrats
        if hasattr(user, 'candidat'):
            return Contract.objects.filter(candidat=user.candidat)
        return Contract.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        # Seul un restaurant peut créer un contrat
        if not hasattr(user, 'restaurant'):
            raise serializers.ValidationError("Seuls les restaurants peuvent générer des contrats.")

        restaurant = user.restaurant
        candidat_id = self.request.data.get('candidat')
        if not candidat_id:
            raise serializers.ValidationError({"candidat": "Le candidat est obligatoire pour générer un contrat."})

        # Valider si le candidat existe
        try:
            candidat = Candidat.objects.get(id=candidat_id)
        except Candidat.DoesNotExist:
            raise serializers.ValidationError({"candidat": "Le candidat spécifié n'existe pas."})

        # Créer le contrat
        serializer.save(restaurant=restaurant, candidat=candidat)
