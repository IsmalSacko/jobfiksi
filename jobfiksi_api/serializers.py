from rest_framework import serializers
from .models import CustomUser, Offre, Ville

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'user_type']
        # Incluez 'password' si vous souhaitez gérer le mot de passe
        extra_kwargs = {'password': {'write_only': True}} # Pour que le mot de passe ne soit pas affiché
    



    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            user_type=validated_data['user_type']
        )
        user.set_password(validated_data['password'])  # N'oubliez pas de hasher le mot de passe
        user.save()
        return user


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


