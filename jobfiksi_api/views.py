from rest_framework import generics, permissions
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from rest_framework import serializers
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .serializers import LoginSerializer
from rest_framework.authtoken.models import Token
from .models import User, Candidat, Restaurant, Ville,Annonce, Candidature, PreferenceCandidat, PreferenceRestaurant, Offre, CustomUser
from .serializers import (
    UserCreateSerializer,
    CandidatSerializer,
    RestaurantSerializer,
    AnnonceSerializer,
    CandidatureSerializer,
    PreferenceCandidatSerializer,
    PreferenceRestaurantSerializer,
    OffreSerializer,
    LoginSerializer,
    VilleSerializer
)

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return render(request, 'jobfiksi_api/auth/register.html')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Vérifiez si un profil existe déjà pour cet utilisateur
            if user.user_type == 'restaurant':
                restaurant_profile, created = Restaurant.objects.get_or_create(user=user)

                if not created:
                    # Mettre à jour le profil existant si nécessaire
                    restaurant_profile.nom = user.username  # Mettez à jour le nom si nécessaire
                    restaurant_profile.adresse = 'Adresse par défaut'  # Mettez à jour l'adresse si nécessaire
                    restaurant_profile.tel = '0123456789'  # Mettez à jour le téléphone si nécessaire
                    restaurant_profile.type = CustomUser.objects.get(id=user.id).user_type  # Mettez à jour le type si nécessaire
                    restaurant_profile.save()
                
            elif user.user_type == 'candidat':
                candidat_profile, created = Candidat.objects.get_or_create(user=user)

                if not created:
                    # Mettre à jour le profil existant si nécessaire
                    candidat_profile.nom = user.username  # Mettez à jour le nom si nécessaire
                    candidat_profile.tel = '0123456789'  # Mettez à jour le téléphone si nécessaire
                    candidat_profile.adresse = 'Adresse par défaut'  # Mettez à jour l'adresse si nécessaire
                    candidat_profile.date_naissance = '2000-01-01'  # Mettez à jour la date de naissance si nécessaire
                    candidat_profile.niveau_etude = 'Niveau d\'étude par défaut'  # Mettez à jour le niveau d'étude si nécessaire
                    candidat_profile.experience = 'Expérience par défaut'  # Mettez à jour l'expérience si nécessaire
                    candidat_profile.ville = Ville.objects.first()  # Mettez à jour la ville si nécessaire
                    candidat_profile.user_type = CustomUser.objects.get(id=user.id).user_type  # Mettez à jour le type si nécessaire
                    candidat_profile.save()

            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)

            response_data = {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'user_type': user.user_type,
                },
                'token': token.key,
                'redirect_url': '/login/',
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    
# Vue pour récupérer les détails d'un candidat
class CandidatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer
    permission_classes = [permissions.IsAuthenticated]



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


class VilleListCreateView(generics.ListCreateAPIView):
    serializer_class = VilleSerializer
    

    def get_queryset(self):
        # Récupérer toutes les villes
        villes = list(Ville.objects.all())
        
        # Récupérer la ville de l'utilisateur connecté
        if self.request.user.is_authenticated and hasattr(self.request.user, 'ville'):
            ville_utilisateur = self.request.user.ville
        else:
            ville_utilisateur = None

        # Trier les villes en mettant la ville de l'utilisateur en premier
        if ville_utilisateur in villes:
            villes.remove(ville_utilisateur)
            villes.insert(0, ville_utilisateur)

        return villes

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Vue pour gérer les annonces
class AnnonceListCreateView(generics.ListCreateAPIView):
    queryset = Annonce.objects.all()
    serializer_class = AnnonceSerializer
    permission_classes = [permissions.AllowAny]  # Seuls les utilisateurs authentifiés peuvent créer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)  # L'utilisateur connecté qui crée l'annonce

class AnnonceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Annonce.objects.all()
    serializer_class = AnnonceSerializer
    permission_classes = [permissions.IsAuthenticated]

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


from django.views.decorators.csrf import csrf_exempt

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return render(request, 'jobfiksi_api/auth/login.html')

    @csrf_exempt  # Désactiver la vérification CSRF pour cette méthode
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Déconnecter l'utilisateur s'il est déjà connecté
        if request.user.is_authenticated:
            logout(request)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Connecter l'utilisateur et créer la session
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)

            # Déterminer l'URL de redirection
            redirect_url = '/profile/candidate/' if user.user_type == 'candidate' else '/profile/restaurant/'

            return Response({
                'token': token.key,
                'user': {'username': user.username},
                'redirect_url': redirect_url
            }, status=status.HTTP_200_OK)

        # Journaliser l'échec d'authentification
        print(f"Authentication failed for username: {username}")
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


    
class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    # def get(self, request):
    #     if request.user.is_authenticated:
    #         logout(request)
    #     return redirect('login')  # Redirige toujours vers la page de connexion
    @csrf_exempt
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('login')  # Redirige toujours vers la page de connexion
@csrf_exempt
def profileDetail(request):
    return render(request, 'jobfiksi_api/auth/profile.html')


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Candidature, Annonce
from .serializers import CandidatureSerializer

class PostulerAnnonceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        """
        Seuls les candidats peuvent postuler à une annonce.
        """
        if request.user.user_type == 'candidat':
            try:
                annonce = Annonce.objects.get(pk=pk)
                candidature_data = {
                    'user': request.user.id,
                    'annonce': annonce.id,
                }
                serializer = CandidatureSerializer(data=candidature_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Annonce.DoesNotExist:
                return Response({'detail': 'Annonce non trouvée.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': 'Vous devez être candidat pour postuler à une annonce.'}, status=status.HTTP_403_FORBIDDEN)


def home(request):
    return render(request, 'jobfiksi_api/home.html')