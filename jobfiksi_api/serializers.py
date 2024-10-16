from rest_framework import serializers
from .models import CustomUser, Offre, Ville

class CustomUserSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_type',]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'date_naissance': {'required': False}
        }

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            # acceptr une chaîne de caractères pour le type d'utilisateur
            user_type= str(validated_data.get('user_type', '')), 
            date_naissance=validated_data.get('date_naissance', None)
        )
        user.set_password(validated_data.get('password'))  # Hachage du mot de passe
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.user_type = validated_data.get('user_type', instance.user_type)
        instance.date_naissance = validated_data.get('date_naissance', instance.date_naissance)

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)  # Hachage du mot de passe

        instance.save()
        return instance



class VilleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ville
        fields = ['id', 'nom', 'code_postal']

class OffreSerializer(serializers.ModelSerializer):
    localisation = VilleSerializer()
    user = serializers.CharField()  # Accepte une chaîne de caractères pour l'utilisateur

    class Meta:
        model = Offre
        fields = ['titre', 'description', 'salaire', 'localisation', 'user']

    def create(self, validated_data):
        localisation_data = validated_data.pop('localisation')
        localisation, created = Ville.objects.get_or_create(**localisation_data)

        # Récupère l'utilisateur par le nom d'utilisateur ou l'email
        user_identifier = validated_data.pop('user')
        try:
            user = CustomUser.objects.get(username=user_identifier)  # ou email=user_identifier
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("L'utilisateur spécifié n'existe pas.")

        offre = Offre.objects.create(localisation=localisation, user=user, **validated_data)
        return offre

    def update(self, instance, validated_data):
        localisation_data = validated_data.pop('localisation', None)
        if localisation_data:
            ville, created = Ville.objects.get_or_create(**localisation_data)
            instance.localisation = ville
        instance.titre = validated_data.get('titre', instance.titre)
        instance.description = validated_data.get('description', instance.description)
        instance.salaire = validated_data.get('salaire', instance.salaire)
        instance.save()
        return instance


