from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Offre, CustomUser

from .serializers import OffreSerializer, CustomUserSerializer


# Create your views here.
class OffreViewSet(viewsets.ModelViewSet):
    queryset = Offre.objects.all()
    serializer_class = OffreSerializer
    permission_classes = [IsAuthenticated]

    # Limiter l'accès pour que seuls les utilisateurs "offrants" puissent créer/modifier des offres


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]  # Seul un admin peut voir/modifier les utilisateurs du site
