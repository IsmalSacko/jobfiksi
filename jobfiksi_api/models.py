from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings


class Adresse(models.Model):
    rue = models.CharField(max_length=255)
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=10)
    pays = models.CharField(max_length=100)

    # Si vous souhaitez lier l'adresse à un utilisateur ou à une annonce
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='adresses')

    def __str__(self):
        return f"{self.rue}, {self.ville}, {self.code_postal}, {self.pays}"


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
    disponibilite = models.TextField(null=True, blank=True)
    plage_horaire = models.CharField(max_length=255, null=True, blank=True)
    niveau_etude = models.CharField(max_length=100, null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    compentence = models.TextField(null=True, blank=True)
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

    def __str__(self):
        return f"{self.nom} {self.prenom} {self.tel} {self.ville}"


# Modèle Restaurant
class Restaurant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='restaurant_profile')
    nom = models.CharField(max_length=100)
    tel = models.CharField(max_length=20, null=True, blank=True)
    email_pro = models.EmailField(null=True, blank=True)
    type = models.CharField(max_length=100)
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
    type_annonce = models.CharField(max_length=100, null=True, blank=True)
    salaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    temps_travail = models.CharField(max_length=10, choices=TEMPS_TRAVAIL_CHOICES)
    nb_heures_semaine = models.IntegerField(null=True, blank=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='annonces')
    # Champs de géolocalisation
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    avantages = models.TextField(null=True, blank=True)
    mode_paiement = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.titre


# models.py
class Chat(models.Model):
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.candidat.nom} and {self.restaurant.nom}"

    @property
    def last_message(self):
        # Retourne le dernier message du chat
        return self.messages.order_by('-created_at').first()

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)  # Utilisateur qui envoie le message
    content = models.TextField()  # Contenu du message
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création du message
    file = models.FileField(upload_to='chat_files/', null=True, blank=True)

    def __str__(self):
        return f"Message from {self.sender.username}: {self.content[:20]}..."


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
