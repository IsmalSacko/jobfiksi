from django.db import models
from django.contrib.auth.models import AbstractUser

# Modèle de la ville
class Ville(models.Model):
    nom = models.CharField(max_length=100) # Nom de la ville(varchar(100))
    # Code postal de la ville(varchar(10))
    code_postal = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nom} ({self.code_postal})"

# Type d'utilisateur : Demandeur ou Offrant
class CustomUser(AbstractUser):
    # Choix du type d'utilisateur
    USER_TYPE_CHOICES = (('candidate', 'Candidat'), ('recuteur', 'Recruteur'),)
    # Champ user_type avec les choix
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='candidat')
    # Champ email unique
    email = models.EmailField(unique=True) 
    

# Moddel de l'offre d'emploi
class Offre(models.Model):
    titre = models.CharField(max_length=200) # Titre de l'offre(varchar(200))
    description = models.TextField() # Description de l'offre(text)
    # Localisation de l'offre
    salaire = models.IntegerField() # Salaire de l'offre(int)
    localisation = models.ForeignKey(Ville, on_delete=models.CASCADE) 
     # Date de création de l'offre
    date_creation = models.DateTimeField(auto_now_add=True)
    # Utilisateur qui a créé l'offre (clé étrangère vers CustomUser)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 


