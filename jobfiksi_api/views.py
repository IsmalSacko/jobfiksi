from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from rest_framework import status
from .models import CustomUser, Offre
from .serializers import CustomUserSerializer, OffreSerializer, VilleSerializer, OffreSerializer
from .permissions import IsRecruiter, IsCandidate  # Permissions personnalisées à implémenter
from rest_framework.views import APIView
from django.shortcuts import render



# Vues pour CustomUser

# Vue générale pour la liste et la création des utilisateurs (tous types confondus)
class CustomUserListCreateView(generics.ListCreateAPIView):
    """
    Permet de lister et de créer des utilisateurs, tout en générant un token
    pour un utilisateur nouvellement créé et le connecter automatiquement.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]  # Autoriser tout le monde à s'inscrire

    def create(self, request, *args, **kwargs):
        # Appeler la méthode create du serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Créer un token pour l'utilisateur nouvellement créé
        token, created = Token.objects.get_or_create(user=user)

        # Connecter l'utilisateur automatiquement
        login(request, user)
        
        

        # Retourner les détails de l'utilisateur avec le token
        return Response({
            "user": CustomUserSerializer(user).data,
            "token": token.key
            

        }, status=status.HTTP_201_CREATED)

# Vue générale pour les détails, mise à jour, et suppression des utilisateurs
class CustomUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Permet de récupérer, mettre à jour ou supprimer un utilisateur.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

# Liste et création des recruteurs
class RecruiterListCreateView(generics.ListCreateAPIView):
    """
    Permet de lister et créer uniquement des utilisateurs de type recruteur.
    """
    queryset = CustomUser.objects.filter(user_type='recuteur')
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsRecruiter]

# Liste et création des candidats
class CandidateListCreateView(generics.ListCreateAPIView):
    """
    Permet de lister et créer uniquement des utilisateurs de type candidat.
    """
    queryset = CustomUser.objects.filter(user_type='candidate')
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsCandidate]

# Détail, mise à jour et suppression d'un recruteur
class RecruiterDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Permet de récupérer, mettre à jour ou supprimer un utilisateur recruteur.
    """
    queryset = CustomUser.objects.filter(user_type='recuteur')
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsRecruiter]

# Détail, mise à jour et suppression d'un candidat
class CandidateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Permet de récupérer, mettre à jour ou supprimer un utilisateur candidat.
    """
    queryset = CustomUser.objects.filter(user_type='candidate')
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsCandidate]

# Vues pour Offre (uniquement pour recruteurs)
class OffreListCreateView(generics.ListCreateAPIView):
    queryset = Offre.objects.all()
    serializer_class = OffreSerializer
    permission_classes = [IsAuthenticated, IsRecruiter]   



    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class OffreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offre.objects.all()
    serializer_class = OffreSerializer
    permission_classes = [IsAuthenticated, IsRecruiter]


# views.py
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView

class LoginView(APIView):
    """
    Permet aux utilisateurs de se connecter et de recevoir un token.
    """
    permission_classes = [AllowAny]  # Autoriser tout le monde à se connecter

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Créer un token si l'utilisateur existe
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Identifiants invalides."}, status=status.HTTP_400_BAD_REQUEST)


def login_view(request):
    """
    Affiche le formulaire de connexion.
    """
    return render(request, 'jobfiksi_api/auth/login.html')

def profile_view(request):
    """
    Affiche le profil de l'utilisateur connecté.
    """
    return render(request, 'jobfiksi_api/auth/profile.html')

def register_view(request):
    """
    Affiche le formulaire d'inscription.
    """
    return render(request, 'jobfiksi_api/auth/register.html')


class UserTypeList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user_types = ['candidat', 'recruteur']  # Remplacez par les types d'utilisateur de votre base de données si nécessaire
        return Response(user_types)