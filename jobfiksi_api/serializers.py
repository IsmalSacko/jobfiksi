from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Candidat, Restaurant, Annonce, Candidature, Adresse, PreferenceCandidat, PreferenceRestaurant, Offre


class AdresseSerializer(serializers.ModelSerializer):
    # created_by = serializers.ReadOnlyField(source='created_by.username')
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
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Candidat
        fields = [
            'id',  # Ajout de l'id pour permettre la mise à jour
            'nom', 'prenom', 'tel', 'date_naissance', 'genre',
            'cv', 'lettre_motivation', 'autres_documents', 'niveau_etude',
            'compentence', 'experience', 'etablissement', 'formation', 'date_debut',
            'date_fin', 'image', 'ville', 'num_et_rue', 'code_postal', 'pays', 'disponibilite',
            'preference_salaire', 'salaire_min', 'salaire_max',
            'plage_horaire', 'iban', 'secu_sociale', 'notification_mail',
        ]

    def update(self, instance, validated_data):
        # Mise à jour des fichiers uniquement si un fichier est fourni dans validated_data
        if 'cv' in validated_data and validated_data['cv'] is not None:
            instance.cv = validated_data['cv']

        if 'lettre_motivation' in validated_data and validated_data['lettre_motivation'] is not None:
            instance.lettre_motivation = validated_data['lettre_motivation']

        if 'autres_documents' in validated_data and validated_data['autres_documents'] is not None:
            instance.autres_documents = validated_data['autres_documents']

        if 'image' in validated_data and validated_data['image'] is not None:
            instance.image = validated_data['image']
        if 'nom' in validated_data and validated_data['nom'] is not None:
            instance.nom = validated_data['nom']
        if 'prenom' in validated_data and validated_data['prenom'] is not None:
            instance.prenom = validated_data['prenom']
        if 'tel' in validated_data and validated_data['tel'] is not None:
            instance.tel = validated_data['tel']
        if 'date_naissance' in validated_data and validated_data['date_naissance'] is not None:
            instance.date_naissance = validated_data['date_naissance']
        if 'genre' in validated_data and validated_data['genre'] is not None:
            instance.genre = validated_data['genre']
        if 'ville' in validated_data and validated_data['ville'] is not None:
            instance.ville = validated_data['ville']
        if 'num_et_rue' in validated_data and validated_data['num_et_rue'] is not None:
            instance.num_et_rue = validated_data['num_et_rue']
        if 'code_postal' in validated_data and validated_data['code_postal'] is not None:
            instance.code_postal = validated_data['code_postal']
        if 'pays' in validated_data and validated_data['pays'] is not None:
            instance.pays = validated_data['pays']
        if 'iban' in validated_data and validated_data['iban'] is not None:
            instance.iban = validated_data['iban']
        if 'secu_sociale' in validated_data and validated_data['secu_sociale'] is not None:
            instance.secu_sociale = validated_data['secu_sociale']
        if 'disponibilite' in validated_data and validated_data['disponibilite'] is not None:
            instance.disponibilite = validated_data['disponibilite']
        if 'plage_horaire' in validated_data and validated_data['plage_horaire'] is not None:
            instance.plage_horaire = validated_data['plage_horaire']
        if 'niveau_etude' in validated_data and validated_data['niveau_etude'] is not None:
            instance.niveau_etude = validated_data['niveau_etude']
        if 'experience' in validated_data and validated_data['experience'] is not None:
            instance.experience = validated_data['experience']
        if 'compentence' in validated_data and validated_data['compentence'] is not None:
            instance.compentence = validated_data['compentence']
        if 'formation' in validated_data and validated_data['formation'] is not None:
            instance.formation = validated_data['formation']
        if 'etablissement' in validated_data and validated_data['etablissement'] is not None:
            instance.etablissement = validated_data['etablissement']
        if 'date_debut' in validated_data and validated_data['date_debut'] is not None:
            instance.date_debut = validated_data['date_debut']
        if 'date_fin' in validated_data and validated_data['date_fin'] is not None:
            instance.date_fin = validated_data['date_fin']
        if 'preference_salaire' in validated_data and validated_data['preference_salaire'] is not None:
            instance.preference_salaire = validated_data['preference_salaire']
        if 'salaire_min' in validated_data and validated_data['salaire_min'] is not None:
            instance.salaire_min = validated_data['salaire_min']
        if 'salaire_max' in validated_data and validated_data['salaire_max'] is not None:
            instance.salaire_max = validated_data['salaire_max']
        if 'notification_mail' in validated_data and validated_data['notification_mail'] is not None:
            instance.notification_mail = validated_data['notification_mail']

        # Mise à jour des autres champs
        for field in [
            'nom', 'prenom', 'tel', 'date_naissance', 'niveau_etude',
            'compentence', 'experience', 'etablissement', 'formation',
            'date_debut', 'date_fin', 'ville', 'num_et_rue', 'code_postal', 'pays',
            'disponibilite', 'plage_horaire', 'iban', 'secu_sociale',
            'preference_salaire', 'salaire_min', 'salaire_max',
            'notification_mail', 'genre'
        ]:
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))

        # Sauvegarde de l'instance après la mise à jour
        instance.save()
        return instance


class RestaurantSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.CharField(source='user.user_type', read_only=True)

    class Meta:
        model = Restaurant

        fields = [
            'id',  # Ajout de l'id pour permettre la mise à jour
            'nom',
            'email_pro',
            'tel',
            'ville',
            'image',
            'num_et_rue',
            'ville',
            'code_postal',
            'pays',
            'site_web',
            'notification_mail',
            'type'

        ]

    def update(self, instance, validated_data):
        # Mise à jour de l'image uniquement si un fichier est fourni dans validated_data
        if 'image' in validated_data and validated_data['image'] is not None:
            instance.image = validated_data['image']
        if 'email_pro' in validated_data and validated_data['email_pro'] is not None:
            instance.email_pro = validated_data['email_pro']
        if 'tel' in validated_data and validated_data['tel'] is not None:
            instance.tel = validated_data['tel']
        if 'ville' in validated_data and validated_data['ville'] is not None:
            instance.ville = validated_data['ville']
        if 'num_et_rue' in validated_data and validated_data['num_et_rue'] is not None:
            instance.num_et_rue = validated_data['num_et_rue']
        if 'code_postal' in validated_data and validated_data['code_postal'] is not None:
            instance.code_postal = validated_data['code_postal']
        if 'pays' in validated_data and validated_data['pays'] is not None:
            instance.pays = validated_data['pays']
        if 'site_web' in validated_data and validated_data['site_web'] is not None:
            instance.site_web = validated_data['site_web']
        if 'notification_mail' in validated_data and validated_data['notification_mail'] is not None:
            instance.notification_mail = validated_data['notification_mail']

        # Mise à jour des autres champs
        for field in [
            'nom', 'email_pro', 'tel', 'ville', 'num_et_rue', 'code_postal', 'pays', 'site_web', 'notification_mail'
        ]:
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))

        # Sauvegarde de l'instance après la mise à jour
        instance.save()
        return instance


class AnnonceSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')  # Récupère le nom d'utilisateur
    ville = serializers.StringRelatedField(source='ville.nom', read_only=True)

    class Meta:
        model = Annonce
        fields = ['id', 'titre', 'description', 'date_publication', 'type_contrat', 'salaire', 'temps_travail',
                  'statut',
                  'created_by', 'ville', 'latitude', 'longitude']


class CandidatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidature
        fields = ['candidat', 'annonce', 'date_candidature']


class PreferenceCandidatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferenceCandidat
        fields = ['candidat', 'flexibilite_deplacement', 'secteur', 'type_contrat', 'type_restaurant',
                  'horaire_travail', 'possibilite_formation', 'possibilite_contrat_direct']


class PreferenceRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferenceRestaurant
        fields = ['restaurant', 'niveau_etude', 'possibilite_former', 'possibilite_debutant', 'horaire_travail']


class OffreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offre
        fields = ['annonce']
