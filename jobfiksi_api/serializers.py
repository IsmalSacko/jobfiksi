from rest_framework import serializers
from .models import CustomUser, Offre

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'user_type']
        # Incluez 'password' si vous souhaitez gérer le mot de passe

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            user_type=validated_data['user_type']
        )
        user.set_password(validated_data['password'])  # N'oubliez pas de hasher le mot de passe
        user.save()
        return user

class OffreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offre
        fields = ['id', 'titre', 'description', 'salaire', 'localisation', 'date_creation', 'user']
