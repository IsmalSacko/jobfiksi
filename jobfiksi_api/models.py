from django.db import models
from django.contrib.auth.models import AbstractUser

# Type d'utilisateur : Demandeur ou Offrant
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('candidate', 'Candidat'),
        ('recuteur', 'Recruteur'),
       )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='candidat')
    # Optionnel : pour que le superuser soit créé sans mot de passe explicite lors de la création via l'admin ou API
    

# Moddel de l'offre d'emploi
class Offre(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    salaire = models.IntegerField()
    localisation = models.CharField(max_length=200)
    date_creation = models.DateTimeField(auto_now_add=True)
    # Relation avec un utilisateur offrant (entreprise)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

