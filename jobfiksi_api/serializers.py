from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Candidat, Restaurant, Annonce, Candidature, Adresse, PreferenceCandidat, PreferenceRestaurant, Offre

class AdresseSerializer(serializers.ModelSerializer):
    #created_by = serializers.ReadOnlyField(source='created_by.username')
    rue = serializers.CharField(required=False, allow_blank=True)
    ville = serializers.CharField(required=False, allow_blank=True)
    code_postal = serializers.CharField(required=False, allow_blank=True)
    pays = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = Adresse
        fields = ['rue', 'ville', 'code_postal', 'pays']
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
    adresse = serializers.PrimaryKeyRelatedField(queryset=Adresse.objects.all(), required=False)
    adresse_data = AdresseSerializer(write_only=True, required=False)
    type = serializers.CharField(read_only=True)
    class Meta:
        model = Candidat
        fields = ['nom', 'prenom', 'tel', 'date_naissance', 'adresse', 'adresse', 'cv', 'niveau_etude', 'experience', 'adresse_data', 'type']

    def update(self, instance, validated_data):
        adresse_data = validated_data.pop('adresse_data', None) # Récupérer les données de l'adresse

        # Mettre à jour les champs du candidat
        instance.nom = validated_data.get('nom', instance.nom)
        instance.prenom = validated_data.get('prenom', instance.prenom)
        instance.tel = validated_data.get('tel', instance.tel)
        instance.date_naissance = validated_data.get('date_naissance', instance.date_naissance)
        instance.cv = validated_data.get('cv', instance.cv)
        instance.niveau_etude = validated_data.get('niveau_etude', instance.niveau_etude)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.save()

        # Mettre à jour ou créer une nouvelle adresse seulement si des champs sont fournis
        if adresse_data and any(adresse_data.values()):
            adresse = instance.adresse
            if adresse:
                # Mettre à jour l'adresse existante
                adresse.rue = adresse_data.get('rue', adresse.rue)
                adresse.ville = adresse_data.get('ville', adresse.ville)
                adresse.code_postal = adresse_data.get('code_postal', adresse.code_postal)
                adresse.pays = adresse_data.get('pays', adresse.pays)
                adresse.save()
            else:
                # Créer une nouvelle adresse et lier automatiquement l'utilisateur connecté
                adresse = Adresse.objects.create(**adresse_data, created_by=self.context['request'].user)
                instance.adresse = adresse
                instance.save()

        return instance


class RestaurantSerializer(serializers.ModelSerializer):
    adresse = serializers.PrimaryKeyRelatedField(queryset=Adresse.objects.all(), allow_null=True, required=False)
    adresse_data = AdresseSerializer(write_only=True, required=False)
    type = serializers.CharField(read_only=True)

    class Meta:
        model = Restaurant
        fields = ['nom', 'tel', 'adresse', 'adresse_data', 'type']

    def update(self, instance, validated_data):
        adresse_data = validated_data.pop('adresse_data', None) # Récupérer les données de l'adresse
       

        # Mettre à jour les champs du restaurant
        instance.nom = validated_data.get('nom', instance.nom)
        instance.tel = validated_data.get('tel', instance.tel)
        instance.save()

        # Mettre à jour ou créer une nouvelle adresse seulement si des champs sont fournis
        if adresse_data and any(adresse_data.values()):
            adresse = instance.adresse
            if adresse:
                # Mettre à jour l'adresse existante
                adresse.rue = adresse_data.get('rue', adresse.rue)
                adresse.ville = adresse_data.get('ville', adresse.ville)
                adresse.code_postal = adresse_data.get('code_postal', adresse.code_postal)
                adresse.pays = adresse_data.get('pays', adresse.pays)
                adresse.save()
            else:
                # Créer une nouvelle adresse et lier automatiquement l'utilisateur connecté
                adresse = Adresse.objects.create(**adresse_data, created_by=self.context['request'].user)
                instance.adresse = adresse
                instance.save()

        return instance


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


