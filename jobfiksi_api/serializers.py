from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Candidat, Restaurant, Annonce, Candidature, Message, Conversation, Contract, CustomUser, \
    FichierJointMessage


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
        user_type = validated_data.pop('user_type')

        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=user_type
        )

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
            'id', 'user', 'nom', 'prenom', 'tel', 'date_naissance', 'cv', 'nationalite',
            'formations', 'experiences', 'niveau_etude', 'flexibilite_deplacement',
            'secteur', 'fourchette_salaire', 'type_contrat', 'type_restaurant',
            'horaire_travail', 'possibilite_formation', 'salaire_min', 'salaire_max',
            'num_et_rue', 'ville', 'code_postal', 'pays', 'iban', 'secu_sociale',
            'lettre_motivation', 'autres_documents', 'image', 'genre', 'disponibilite',
            'specilaite', 'langues_parlees', 'type_de_poste_recherche',
            'type_de_contrat_recherche', 'preference_lieu', 'email_pro', 'preference_salaire',
            'notification_mail', 'profil_public'
        ]

    def update(self, instance, validated_data):
        # Gestion des fichiers : Conserver l'ancien fichier si aucun nouveau n'est soumis
        for file_field in ['lettre_motivation', 'autres_documents', 'image', 'cv']:
            if file_field in validated_data:
                # Si le fichier est `None`, conserver l'ancienne valeur
                if validated_data[file_field] is None:
                    validated_data[file_field] = getattr(instance, file_field)

        # Mise à jour des autres champs
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RestaurantSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    # Personnalisation des champs datetime
    creneau_1 = serializers.DateTimeField(format="%d/%m/%Y : %H:%M", required=False, allow_null=True)
    creneau_2 = serializers.DateTimeField(format="%d/%m/%Y : %H:%M", required=False, allow_null=True)
    creneau_3 = serializers.DateTimeField(format="%d/%m/%Y : %H:%M", required=False, allow_null=True)

    class Meta:
        model = Restaurant
        fields = [
            'id', 'user', 'nom', 'tel', 'email_pro', 'type_de_restaurant',
            'image', 'num_et_rue', 'ville', 'code_postal', 'pays', 'site_web',
            'notification_mail', 'niveau_etude', 'age_min', 'attente_candidat',
            'possibilite_former', 'type_de_contrat', 'type_de_travail', 'possibilite_debuter',
            'horaire_travail', 'creneau_1', 'creneau_2', 'creneau_3'
        ]

    def update(self, instance, validated_data):
        # Gestion du fichier image : conserver l'ancienne valeur si aucun nouveau fichier n'est soumis
        if 'image' in validated_data:
            if validated_data['image'] is None:
                validated_data['image'] = instance.image  # Conserver l'ancienne image
        for creneau in ['creneau_1', 'creneau_2', 'creneau_3']:
            if creneau in validated_data:
                if validated_data[creneau] is None:
                    validated_data[creneau] = getattr(instance, creneau)

        # Mise à jour des autres champs
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class AnnonceSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Annonce
        fields = ['id', 'created_by', 'titre', 'description', 'date_publication', 'type_contrat', 'type_annonce',
                  'salaire', 'temps_travail', 'statut', 'ville', 'code_postal', 'pays', 'avantages',
                  'nb_heures_semaine',
                  'horaire_travail', 'jours_de_travail', 'mode_paiement', 'experience']

    def get_created_by(self, obj):
        return obj.created_by.username


class CandidatureSerializer(serializers.ModelSerializer):
    candidat = serializers.StringRelatedField(read_only=True)  # Toujours en lecture seule
    annonce = serializers.PrimaryKeyRelatedField(
        queryset=Annonce.objects.all(),  # Permet de choisir une annonce existante
    )

    class Meta:
        model = Candidature
        fields = '__all__'
        read_only_fields = ['date_candidature', 'candidat']

    def update(self, instance, validated_data):
        statut = validated_data.get('statut', None)
        note = validated_data.get('note', None)

        if statut is not None:
            instance.statut = statut
        if note is not None:
            instance.note = note

        instance.save()
        return instance


class ContractSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.nom', read_only=True)
    candidat_name = serializers.CharField(source='candidat.nom', read_only=True)

    class Meta:
        model = Contract
        fields = [
            'id', 'restaurant', 'candidat', 'restaurant_name', 'candidat_name',
            'date_signature', 'date_debut', 'date_fin', 'type_contrat',
            'salaire', 'horaire_travail', 'statut', 'restaurant_comments',
            'candidat_comments'
        ]
        read_only_fields = ['statut', 'restaurant_name', 'candidat_name']


class FichierJointSerializer(serializers.ModelSerializer):
    class Meta:
        model = FichierJointMessage
        fields = ['id', 'fichier', 'taille', 'type_fichier']


class ConversationSerializer(serializers.ModelSerializer):
    premier_message = serializers.CharField(max_length=1000, write_only=True, required=False)
    fichiers_joints = serializers.FileField(write_only=True, required=False)  # Simple FileField
    # candidat = utilisateur connecté


    class Meta:
        model = Conversation
        fields = ['id', 'candidat', 'restaurant', 'date_creation', 'statut', 'premier_message', 'fichiers_joints']
        read_only_fields = ['id', 'date_creation', 'statut']

    def create(self, validated_data):
        premier_message = validated_data.pop('premier_message', None)
        fichier_joint = validated_data.pop('fichiers_joints', None)  # Récupère un seul fichier
        conversation = Conversation.objects.create(**validated_data)

        # Ajouter le premier message
        if premier_message:
            message = Message.objects.create(
                conversation=conversation,
                auteur=self.context['request'].user,
                contenu=premier_message,
                type_message='text'
            )

            # Ajouter le fichier joint s'il existe
            if fichier_joint:
                FichierJointMessage.objects.create(
                    message=message,
                    fichier=fichier_joint,
                    taille=fichier_joint.size,
                    type_fichier=fichier_joint.content_type
                )

        return conversation


class MessageSerializer(serializers.ModelSerializer):
    fichiers_joints = serializers.FileField(write_only=True, required=False)  # Un seul fichier à la fois

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'contenu', 'type_message', 'date_envoi', 'fichiers_joints']
        read_only_fields = ['id', 'date_envoi']

    def create(self, validated_data):
        fichier_joint = validated_data.pop('fichiers_joints', None)
        message = Message.objects.create(**validated_data)

        if fichier_joint:
            # Crée un fichier joint pour le message
            FichierJointMessage.objects.create(
                message=message,
                fichier=fichier_joint,
                taille=fichier_joint.size,
                type_fichier=fichier_joint.content_type
            )
        return message
