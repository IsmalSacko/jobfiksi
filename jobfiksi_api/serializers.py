from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Candidat, Restaurant, Annonce, Candidature, PreferenceCandidat, PreferenceRestaurant, Offre, Ville

from rest_framework import serializers
class VilleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ville
        fields = ['nom']
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_type = validated_data.pop('user_type')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=user_type
        )

        # Créer le profil correspondant selon le type
        if user_type == 'candidat':
            Candidat.objects.create(user=user)
        elif user_type == 'restaurant':
            Restaurant.objects.create(user=user)

        return user

class CandidatSerializer(serializers.ModelSerializer):
    ville = serializers.CharField(source='ville.nom', read_only=True)
    class Meta:
        model = Candidat
        fields = ['nom', 'prenom', 'tel', 'date_naissance', 'adresse', 'ville', 'cv', 'niveau_etude', 'experience']

class RestaurantSerializer(serializers.ModelSerializer):
    #ville = VilleSerializer(read_only=True)
    ville = serializers.CharField(source='ville.nom', read_only=True)
    class Meta:
        model = Restaurant
        fields = ['nom', 'tel', 'adresse', 'ville', 'type']

class AnnonceSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')  # Récupère le nom d'utilisateur
    ville = serializers.StringRelatedField(source='ville.nom', read_only=True)

    class Meta:
        model = Annonce
        fields = ['titre', 'description', 'date_publication', 'type_contrat', 'salaire', 'temps_travail', 'statut', 'created_by', 'ville']

class CandidatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidature
        fields = ['candidat', 'annonce', 'date_candidature']

class PreferenceCandidatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferenceCandidat
        fields = ['candidat', 'flexibilite_deplacement', 'secteur', 'type_contrat', 'type_restaurant', 'horaire_travail', 'possibilite_formation', 'possibilite_contrat_direct']

class PreferenceRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferenceRestaurant
        fields = ['restaurant', 'niveau_etude', 'possibilite_former', 'possibilite_debutant', 'horaire_travail']

class OffreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offre
        fields = ['annonce']


