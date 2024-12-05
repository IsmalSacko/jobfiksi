from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Candidat, Restaurant, Annonce, Candidature


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=get_user_model().USER_TYPE_CHOICES)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Récupérer le type d'utilisateur
        user_type = validated_data.pop('user_type')

        # Créer l'utilisateur
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=user_type
        )

        # Créer le profil correspondant (Candidat ou Restaurant) en fonction du type
        if user_type == 'candidat':
            Candidat.objects.create(user=user)  # Créer un profil Candidat
        elif user_type == 'restaurant':
            Restaurant.objects.create(user=user)  # Créer un profil Restaurant

        return user


class CandidatSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    age = serializers.ReadOnlyField()

    class Meta:
        model = Candidat
        fields = [
            'id',  # Ajout de l'id pour permettre la mise à jour
            'nom', 'prenom', 'tel', 'date_naissance', 'age', 'genre',
            'cv', 'lettre_motivation', 'autres_documents', 'niveau_etude',
            'specilaite', 'experience', 'etablissement', 'formation', 'date_debut',
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

        # Mise à jour des autres champs
        for field in [
            'nom', 'prenom', 'tel', 'date_naissance', 'niveau_etude',
            'specilaite', 'experience', 'etablissement', 'formation',
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
            'type_de_restaurant',

        ]

    def update(self, instance, validated_data):
        # Mise à jour des autres champs et garder les anciennes valeurs si non fournies
        for field in [
            'nom', 'email_pro', 'tel', 'ville', 'image', 'num_et_rue', 'ville', 'code_postal', 'pays', 'site_web',
            'notification_mail', 'type_de_restaurant'
        ]:
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))

        # Sauvegarde de l'instance après la mise à jour
        instance.save()
        return instance


class AnnonceSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')  # Récupère le nom d'utilisateur

    class Meta:
        model = Annonce
        fields = ['id', 'titre', 'description', 'date_publication', 'type_contrat', 'type_annonce', 'type_de_travail',
                  'salaire', 'temps_travail', 'statut', 'created_by', 'ville', 'code_postal', 'pays',
                  'avantages', 'nb_heures_semaine', 'horaire_travail', 'jours_de_travail', 'mode_paiement',
                  'experience',
                  ]


class CandidatureSerializer(serializers.ModelSerializer):
    candidat_nom = serializers.ReadOnlyField(source='candidat.user.username')
    annonce_titre = serializers.ReadOnlyField(source='annonce.titre')

    class Meta:
        model = Candidature
        fields = ['id', 'candidat', 'candidat_nom', 'annonce', 'annonce_titre',
                  'nom', 'prenom', 'tel', 'email', 'ville', 'code_postal', 'pays',
                  'disponibilite', 'crenaux_horaire', 'date_candidature', 'ad_cv', 'message'
                  ]
        read_only_fields = ['candidat', 'date_candidature', 'annonce_titre', 'candidat_nom']
