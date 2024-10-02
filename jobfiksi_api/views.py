from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import CustomUser, Offre
from .serializers import CustomUserSerializer, OffreSerializer

# Vues pour CustomUser

class CustomUserListCreateView(generics.ListCreateAPIView):
  
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]  # Si vous souhaitez restreindre l'accès

class CustomUserDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

# Vues pour Offre

class OffreListCreateView(generics.ListCreateAPIView):
   
    queryset = Offre.objects.all()
    serializer_class = OffreSerializer
    permission_classes = [IsAuthenticated]  # Si vous souhaitez restreindre l'accès

class OffreDetailView(generics.RetrieveUpdateDestroyAPIView):
   
    queryset = Offre.objects.all()
    serializer_class = OffreSerializer
    permission_classes = [IsAuthenticated]
