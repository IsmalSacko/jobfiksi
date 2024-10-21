from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings


# Modèle de la ville
class Ville(models.Model):
    nom = models.CharField(max_length=100)  # Nom de la ville
    code_postal = models.CharField(max_length=10)  # Code postal de la ville

    def __str__(self):
        # Renvoyer le nom de la ville et les deux premiers chiffres du code postal
        return f"{self.nom} ({self.code_postal[:2]})"

# Modèle CustomUser
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('candidat', 'Candidat'),
        ('restaurant', 'Restaurant'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

# Récupérer le modèle CustomUser
User = get_user_model()

# Modèle Candidat
class Candidat(models.Model):
   
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='candidat_profile')
    
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    tel = models.CharField(max_length=20, null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    adresse = models.CharField(max_length=255, null=True, blank=True)
    ville = models.ForeignKey(Ville, on_delete=models.SET_NULL, null=True, blank=True, related_name='candidats')
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)
    niveau_etude = models.CharField(max_length=100, null=True, blank=True)
    experience = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

# Modèle Restaurant
class Restaurant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='restaurant_profile')
    nom = models.CharField(max_length=100)
    tel = models.CharField(max_length=20, null=True, blank=True)
    adresse = models.CharField(max_length=255)
    ville = models.ForeignKey(Ville, on_delete=models.SET_NULL, null=True, blank=True, related_name='restaurants')
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

# Modèle Annonce
class Annonce(models.Model):
    CDI = 'CDI'
    CDD = 'CDD'
    TYPE_CONTRAT_CHOICES = [
        (CDI, 'CDI'),
        (CDD, 'CDD'),
    ]

    TEMPS_PARTIEL = 'Partiel'
    TEMPS_PLEIN = 'Plein'
    TEMPS_TRAVAIL_CHOICES = [
        (TEMPS_PARTIEL, 'Temps partiel'),
        (TEMPS_PLEIN, 'Temps plein'),
    ]

    URGENT = 'Urgent'
    NON_URGENT = 'Non Urgent'
    STATUT_CHOICES = [
        (URGENT, 'Urgent'),
        (NON_URGENT, 'Non Urgent'),
    ]

    titre = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    date_publication = models.DateTimeField(auto_now_add=True)
    type_contrat = models.CharField(max_length=3, choices=TYPE_CONTRAT_CHOICES)
    salaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    temps_travail = models.CharField(max_length=10, choices=TEMPS_TRAVAIL_CHOICES)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES)
    from django.conf import settings
from django.db import models

class Annonce(models.Model):
    CDI = 'CDI'
    CDD = 'CDD'
    TYPE_CONTRAT_CHOICES = [
        (CDI, 'CDI'),
        (CDD, 'CDD'),
    ]

    TEMPS_PARTIEL = 'Partiel'
    TEMPS_PLEIN = 'Plein'
    TEMPS_TRAVAIL_CHOICES = [
        (TEMPS_PARTIEL, 'Temps partiel'),
        (TEMPS_PLEIN, 'Temps plein'),
    ]

    URGENT = 'Urgent'
    NON_URGENT = 'Non Urgent'
    STATUT_CHOICES = [
        (URGENT, 'Urgent'),
        (NON_URGENT, 'Non Urgent'),
    ]

    titre = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    date_publication = models.DateTimeField(auto_now_add=True)
    type_contrat = models.CharField(max_length=3, choices=TYPE_CONTRAT_CHOICES)
    salaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    temps_travail = models.CharField(max_length=10, choices=TEMPS_TRAVAIL_CHOICES)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='annonces')  # L'utilisateur qui a créé l'annonce

    def __str__(self):
        return self.titre


    def __str__(self):
        return self.titre

# Modèle Candidature
class Candidature(models.Model):
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE, related_name='candidatures')
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='candidatures')
    date_candidature = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Candidature de {self.candidat} pour {self.annonce}"

# Modèle PreferenceCandidat
class PreferenceCandidat(models.Model):
    candidat = models.OneToOneField(Candidat, on_delete=models.CASCADE, related_name='preference')
    flexibilite_deplacement = models.BooleanField(default=False)
    secteur = models.CharField(max_length=100, null=True, blank=True)
    type_contrat = models.CharField(max_length=3, choices=Annonce.TYPE_CONTRAT_CHOICES, null=True, blank=True)
    type_restaurant = models.CharField(max_length=100, null=True, blank=True)
    horaire_travail = models.CharField(max_length=50, null=True, blank=True)
    possibilite_formation = models.BooleanField(default=False)
    possibilite_contrat_direct = models.BooleanField(default=False)

    def __str__(self):
        return f"Préférences de {self.candidat}"

# Modèle PreferenceRestaurant
class PreferenceRestaurant(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, related_name='preference')
    niveau_etude = models.CharField(max_length=100, null=True, blank=True)
    possibilite_former = models.BooleanField(default=False)
    possibilite_debutant = models.BooleanField(default=False)
    horaire_travail = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Préférences pour {self.restaurant}"

# Modèle Offre
class Offre(models.Model):
    annonce = models.OneToOneField(Annonce, on_delete=models.CASCADE, related_name='offre')

    def __str__(self):
        return f"Offre pour {self.annonce}"
