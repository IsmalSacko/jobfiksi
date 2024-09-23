from django.db import models
from django.contrib.auth.models import AbstractUser

# Type d'utilisateur : Demandeur ou Offrant
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('demandeur', 'Demandeur'),
        ('offrant', 'Offrant'),
       )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='demandeur')
        # Éviter les conflits avec les reverse accessors de Django
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Nouveau related_name
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Nouveau related_name
        blank=True,
    )

# Moddel de l'offre d'emploi
class Offre(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    salaire = models.IntegerField()
    localisation = models.CharField(max_length=200)
    date_creation = models.DateTimeField(auto_now_add=True)
    # Relation avec un utilisateur offrant (entreprise)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

