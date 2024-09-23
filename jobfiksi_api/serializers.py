import rest_framework.serializers
from .models import Offre, CustomUser



class OffreSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = Offre
        fields = ['id', 'titre', 'description', 'salaire', 'localisation', 'date_creation', 'user']



from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)  # Mot de passe requis uniquement lors de la création

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'user_type']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data) 
        if password:
            user.set_password(password)
            user.save()
        return user

