from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings


# Modèle CustomUser
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('candidat', 'Candidat'),
        ('restaurant', 'Restaurant'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    class Meta:
        db_table = 'custom_user'
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['id']


# Récupérer le modèle CustomUser
User = get_user_model()


# Modèle Candidat
class Candidat(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='candidat_profile')

    nom = models.CharField(max_length=100, null=True, blank=True)
    prenom = models.CharField(max_length=100, null=True, blank=True)
    tel = models.CharField(max_length=20, null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    # adresse = models.ForeignKey(Adresse, on_delete=models.SET_NULL, null=True, blank=True)
    num_et_rue = models.CharField(max_length=255, null=True, blank=True)
    ville = models.CharField(max_length=100, null=True, blank=True)
    code_postal = models.CharField(max_length=10, null=True, blank=True)
    pays = models.CharField(max_length=100, null=True, blank=True)
    iban = models.CharField(max_length=27, null=True, blank=True)
    secu_sociale = models.CharField(max_length=15, null=True, blank=True)
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)
    lettre_motivation = models.FileField(upload_to='lettres_motivation/', null=True, blank=True)
    autres_documents = models.FileField(upload_to='autres_documents/', null=True, blank=True)
    image = models.ImageField(upload_to='images/candidat', null=True, blank=True)
    genre = models.CharField(max_length=10, null=True, blank=True)
    disponibilite = models.TextField(choices=[
        ('tout de suite', 'Tout de suite'),
        ('dans 3 jours', 'Dans 3 jours'),
        ('dans les prochaines semaines', 'Dans les prochaines semaines'),
        ('dans les prochains mois', 'Dans les prochains mois')], max_length=100, null=True, blank=True)

    plage_horaire = models.CharField(max_length=255, null=True, blank=True)
    niveau_etude = models.CharField(max_length=100, null=True, blank=True)
    experience = models.TextField(max_length=255, null=True, blank=True, choices=[
        ('Plus d\'expereince', 'Plus d\'expereince'),
        ('Moins d\'expereince', 'Moins d\'expereince'),
        ('plus de 1 an', 'plus de 1 an'),
        ('plus de 2 ans', 'plus de 2 ans'),
        ('plus de 5 ans', 'plus de 5 ans'),
        ('plus de 10 ans', 'plus de 10 ans')
    ])
    specilaite = models.CharField(choices=[
        ('serveur', 'Serveur'),
        ('cuisinier', 'Cuisinier'),
        ('livreur', 'Livreur'),
        ('netoyage', 'Netoyage'),
        ('chef', 'Chef')], max_length=100, null=True, blank=True)
    formation = models.CharField(max_length=255, blank=True, null=True)
    etablissement = models.CharField(max_length=100, null=True, blank=True)
    date_debut = models.DateField(blank=True, null=True)
    date_fin = models.DateField(blank=True, null=True)
    langues_parlees = models.CharField(max_length=255, null=True, blank=True)
    type_de_poste_recherche = models.CharField(max_length=100, null=True, blank=True)
    type_de_contrat_recherche = models.CharField(max_length=100, null=True, blank=True)
    preference_lieu = models.CharField(max_length=100, null=True, blank=True)
    salaire_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salaire_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    email_pro = models.EmailField(null=True, blank=True)
    # preférence_salaire en euros
    preference_salaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # notification par mail oui ou non
    notification_mail = models.BooleanField(default=False)
    # Souhaitez-vous rendre votre profil public ?
    profil_public = models.BooleanField(default=False)

    @property
    def age(self):
        today = date.today()
        if self.date_naissance:
            return today.year - self.date_naissance.year - (
                    (today.month, today.day) < (self.date_naissance.month, self.date_naissance.day)
            )
        return None

    def __str__(self):
        return f"{self.nom} {self.prenom} {self.tel} {self.ville}"

    class Meta:
        db_table = 'candidat'


# Modèle Restaurant
class Restaurant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='restaurant_profile')
    nom = models.CharField(max_length=100)
    tel = models.CharField(max_length=20, null=True, blank=True)
    email_pro = models.EmailField(null=True, blank=True)
    type_de_restaurant = models.CharField(choices=[
        ('italien', 'Italien'),
        ('francais', 'Français'),
        ('chinois', 'Chinois'),
        ('japonais', 'Japonais'),
        ('indien', 'Indien'),
        ('fast_food', 'Fast-food'),
        ('brasserie', 'Brasserie'),
        ('toutt', 'Tout')], max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='images/restaurant', null=True, blank=True)
    num_et_rue = models.CharField(max_length=255, null=True, blank=True)
    ville = models.CharField(max_length=100, null=True, blank=True)
    code_postal = models.CharField(max_length=10, null=True, blank=True)
    pays = models.CharField(max_length=100, null=True, blank=True)
    site_web = models.URLField(null=True, blank=True)
    notification_mail = models.BooleanField(default=False)

    def __str__(self):
        # return tous les champs du restaurant
        return f"{self.nom} {self.tel} {self.type} {self.site_web}"

    class Meta:
        db_table = 'restaurant'


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
    ville = models.CharField(max_length=100, null=True, blank=True)
    code_postal = models.CharField(max_length=10, null=True, blank=True)
    pays = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date_publication = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    type_contrat = models.CharField(max_length=3, choices=TYPE_CONTRAT_CHOICES)
    type_annonce = models.CharField(max_length=100, null=True, blank=True)
    salaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    temps_travail = models.CharField(max_length=10, choices=TEMPS_TRAVAIL_CHOICES)
    nb_heures_semaine = models.IntegerField(null=True, blank=True)
    type_de_travail = models.CharField(choices=[
        ('servur', 'Serveur'),
        ('cuisinier', 'Cuisinier'),
        ('livreur', 'Livreur'),
        ('netoyage', 'Netoyage'),
        ('chef', 'Chef'),
        ('caissier', 'Caissier'),
        ('plongeur', 'Plongeur'),
        ('patissier', 'Patissier')], max_length=100, null=True, blank=True)
    jours_de_travail = models.CharField(max_length=100, null=True, blank=True)
    horaire_travail = models.CharField(choices=[
        ('matin', 'Matin : 8h-12h'),
        ('midi', 'Midi : 12h-15h'),
        ('soir', 'Soir : 18h-22h'),
        ('nuit', 'Nuit : 22h-6h')], max_length=100, null=True, blank=True)

    experience = models.CharField(max_length=255, null=True, blank=True, choices=[
        ('Plus d\'expereince', 'Plus d\'expereince'),
        ('Moins d\'expereince', 'Moins d\'expereince'),
        ('plus de 1 an', 'plus de 1 an'),
        ('plus de 2 ans', 'plus de 2 ans'),
        ('plus de 5 ans', 'plus de 5 ans'),
        ('plus de 10 ans', 'plus de 10 ans')
    ])
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='annonces')
    # Champs de géolocalisation
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    avantages = models.TextField(null=True, blank=True)
    mode_paiement = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.titre

    class Meta:
        db_table = 'annonce'


class Candidature(models.Model):
    candidat = models.ForeignKey(
        Candidat,
        on_delete=models.CASCADE,
        related_name='candidatures'
    )
    annonce = models.ForeignKey(
        Annonce,
        on_delete=models.CASCADE,
        related_name='candidatures'
    )
    nom = models.CharField(max_length=100, null=True, blank=True)
    prenom = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    tel = models.CharField(max_length=20, null=True, blank=True)
    ville = models.CharField(max_length=100, null=True, blank=True)
    code_postal = models.CharField(max_length=10, null=True, blank=True)
    pays = models.CharField(max_length=100, null=True, blank=True)
    disponibilite = models.TextField(choices=[
        ('Lundi', 'Lundi'),
        ('Mardi', 'Mardi'),
        ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi'),
        ('Vendredi', 'Vendredi'),
        ('Samedi', 'Samedi'),
        ('Dimanche', 'Dimanche'),
        ('Tous les jours', 'Tous les jours')],max_length=100, null=True, blank=True)
    crenaux_horaire = models.CharField(max_length=255, null=True, blank=True,choices=[
        ('8h-12h', 'Matin : 8h-12h'),
        ('12h-15h', 'Midi : 12h-15h'),
        ('18h-22h', 'Soir : 18h-22h'),
        ('22h-6h', 'Nuit : 22h-6h')],)
    date_candidature = models.DateField(auto_now_add=True)
    ad_cv = models.FileField(upload_to='candidatures/', null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Candidature de {self.candidat} pour {self.annonce}"

    class Meta:
        db_table = 'candidature'
        unique_together = ('candidat', 'annonce')  # Contrainte d'unicité
        verbose_name = 'Candidature'
        verbose_name_plural = 'Candidatures'
        ordering = ['date_candidature']
