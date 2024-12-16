from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.timezone import now


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


class Candidat(models.Model):
    NIVEAU_ETUDE_CHOICES = [
        ('bac', 'Bac'),
        ('bac+2', 'Bac+2'),
        ('bac+3', 'Bac+3'),
        ('bac+5', 'Bac+5'),
        ('autre', 'Autre'),
    ]

    DISPONIBILITE_CHOICES = [
        ('tout de suite', 'Tout de suite'),
        ('dans 3 jours', 'Dans 3 jours'),
        ('dans les prochaines semaines', 'Dans les prochaines semaines'),
        ('dans les prochains mois', 'Dans les prochains mois'),
    ]

    SPECIALITE_CHOICES = [
        ('serveur', 'Serveur'),
        ('cuisinier', 'Cuisinier'),
        ('livreur', 'Livreur'),
        ('nettoyage', 'Nettoyage'),
        ('chef', 'Chef'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='candidat_profile')
    nom = models.CharField(max_length=100, null=True, blank=True)
    prenom = models.CharField(max_length=100, null=True, blank=True)
    tel = models.CharField(max_length=20, null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)

    # Nouveau champ
    nationalite = models.CharField(max_length=100, null=True, blank=True)

    # Formations et expériences
    formations = models.TextField(null=True, blank=True)
    experiences = models.TextField(null=True, blank=True)

    niveau_etude = models.CharField(max_length=100, choices=NIVEAU_ETUDE_CHOICES, null=True, blank=True)
    flexibilite_deplacement = models.BooleanField(default=False)
    secteur = models.CharField(max_length=100, null=True, blank=True)
    fourchette_salaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    type_contrat = models.CharField(max_length=100, null=True, blank=True)
    type_restaurant = models.CharField(max_length=100, null=True, blank=True)
    horaire_travail = models.CharField(max_length=100, null=True, blank=True)
    possibilite_formation = models.BooleanField(default=False)
    salaire_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salaire_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    num_et_rue = models.CharField(max_length=255, null=True, blank=True)
    ville = models.CharField(max_length=100, null=True, blank=True)
    code_postal = models.CharField(max_length=10, null=True, blank=True)
    pays = models.CharField(max_length=100, null=True, blank=True)
    iban = models.CharField(max_length=27, null=True, blank=True)
    secu_sociale = models.CharField(max_length=15, null=True, blank=True)
    lettre_motivation = models.FileField(upload_to='lettres_motivation/', null=True, blank=True)
    autres_documents = models.FileField(upload_to='autres_documents/', null=True, blank=True)
    image = models.ImageField(upload_to='images/candidat', null=True, blank=True)
    genre = models.CharField(max_length=10, null=True, blank=True)
    disponibilite = models.CharField(max_length=100, choices=DISPONIBILITE_CHOICES, null=True, blank=True)
    specilaite = models.CharField(max_length=100, choices=SPECIALITE_CHOICES, null=True, blank=True)
    langues_parlees = models.TextField(null=True, blank=True)
    type_de_poste_recherche = models.CharField(max_length=100, null=True, blank=True)
    type_de_contrat_recherche = models.CharField(max_length=100, null=True, blank=True)
    preference_lieu = models.CharField(max_length=100, null=True, blank=True)
    email_pro = models.EmailField(null=True, blank=True)
    preference_salaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notification_mail = models.BooleanField(default=False)
    profil_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

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

    # Niveau d'étude : liste de niveaux d'études possibles
    NIVEAU_ETUDE_CHOICES = [
        ('bac', 'Bac'),
        ('bac+2', 'Bac+2'),
        ('bac+3', 'Bac+3'),
        ('bac+5', 'Bac+5'),
        ('autre', 'Autre'),
    ]
    niveau_etude = models.CharField(max_length=100, choices=NIVEAU_ETUDE_CHOICES, null=True, blank=True)
    age_min = models.IntegerField(choices=[(18, '18'), (21, '21'), (25, '25'), (30, '30'), (35, '35'), (40, '40')],
                                  null=True, blank=True)
    attente_candidat = models.CharField(max_length=255, null=True, blank=True)
    # Possibilité de former : Booléen
    possibilite_former = models.BooleanField(default=False)

    # Type de contrat : liste de types de contrats possibles
    TYPE_CONTRAT_CHOICES = [
        ('CDI', 'CDI'),
        ('CDD', 'CDD'),
        ('intérim', 'Intérim'),
        ('stage', 'Stage'),
    ]
    type_de_contrat = models.CharField(max_length=100, choices=TYPE_CONTRAT_CHOICES, null=True, blank=True)

    # Type de travail : liste de types de travail possibles
    TYPE_TRAVAIL_CHOICES = [
        ('serveur', 'Serveur'),
        ('cuisinier', 'Cuisinier'),
        ('livreur', 'Livreur'),
        ('nettoyage', 'Nettoyage'),
        ('chef', 'Chef'),
        ('caissier', 'Caissier'),
        ('plongeur', 'Plongeur'),
        ('patissier', 'Patissier'),
    ]
    type_de_travail = models.CharField(max_length=100, choices=TYPE_TRAVAIL_CHOICES, null=True, blank=True)

    # Possibilité de débuter : Booléen
    possibilite_debuter = models.BooleanField(default=False)

    # Horaire de travail : liste d'options possibles pour les horaires
    HORAIRES_TRAVAIL_CHOICES = [
        ('matin', 'Matin'),
        ('midi', 'Midi'),
        ('soir', 'Soir'),
        ('nuit', 'Nuit'),
        ('flexible', 'Flexible'),
    ]
    horaire_travail = models.CharField(max_length=100, choices=HORAIRES_TRAVAIL_CHOICES, null=True, blank=True)
    # creneau_entretien =plusieurs dates possibles pour un entretien
    creneau_1 = models.DateTimeField(null=True, blank=True)
    creneau_2 = models.DateTimeField(null=True, blank=True)
    creneau_3 = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        # return tous les nom et le user_type
        return f"{self.nom} - {self.user.user_type}"

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
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="annonces",
                                   null=True,
                                   blank=True)

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
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE, related_name="candidatures")
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name="candidatures")
    nom = models.CharField(max_length=100, null=True, blank=True)
    prenom = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    tel = models.CharField(max_length=20, null=True, blank=True)
    ville = models.CharField(max_length=100, null=True, blank=True)
    code_postal = models.CharField(max_length=10, null=True, blank=True)
    pays = models.CharField(max_length=100, null=True, blank=True)
    disponibilite = models.TextField(choices=[('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'),
                                              ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi'),
                                              ('Dimanche', 'Dimanche'), ('Tous les jours', 'Tous les jours')],
                                     max_length=100, null=True, blank=True)
    crenaux_horaire = models.CharField(max_length=255, null=True, blank=True, choices=[('8h-12h', 'Matin : 8h-12h'),
                                                                                       ('12h-15h', 'Midi : 12h-15h'),
                                                                                       ('18h-22h', 'Soir : 18h-22h'),
                                                                                       ('22h-6h', 'Nuit : 22h-6h')])
    date_candidature = models.DateField(auto_now_add=True)
    date_entretien = models.DateTimeField(null=True, blank=True)
    cv = models.FileField(upload_to='candidatures/', null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    statut = models.BooleanField(choices=[(True, 'Acceptée'), (False, 'Refusée'), (None, 'En attente')], null=True,
                                 blank=True)
    note = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)  # Note du candidat

    def __str__(self):
        return f"Candidature de {self.candidat} pour {self.annonce}"

    class Meta:
        db_table = 'candidature'
        unique_together = ('candidat', 'annonce')  # Contrainte d'unicité
        verbose_name = 'Candidature'
        verbose_name_plural = 'Candidatures'
        ordering = ['date_candidature']


# Modèle pour les favoris d'un candidat
class CanditatFavoris(models.Model):
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE, related_name="favoris")
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name="favoris")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="favoris")
    favori = models.BooleanField(default=False)

    class Meta:
        db_table = 'candidat_favoris'


class Entretien(models.Model):
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE, related_name="entretiens")
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name="entretiens")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="entretiens")
    date = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=100,
                              choices=[('prévu', 'Prévu'), ('réalisé', 'Réalisé'), ('annulé', 'Annulé')])
    commentaire = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Entretien de {self.candidat.nom} pour {self.annonce.titre} avec {self.restaurant.nom}"

    class Meta:
        db_table = 'entretien'


class Conversation(models.Model):
    candidat = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="conversations_candidat",
        limit_choices_to={'user_type': 'candidat'}  # Filtrer uniquement les candidats
    )
    restaurant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="conversations_restaurant",
        limit_choices_to={'user_type': 'restaurant'}  # Filtrer uniquement les restaurants
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=20,
        choices=[('active', 'Active'), ('closed', 'Closed')],
        default='active'
    )

    def __str__(self):
        return f"Conversation entre {self.candidat.username} et {self.restaurant.username}"

    class Meta:
        db_table = 'conversation'
        unique_together = ('candidat', 'restaurant')  # Une seule conversation possible entre deux utilisateurs


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages_envoyes"
    )  # Auteur : candidat ou restaurant
    contenu = models.TextField(blank=True, null=True)
    type_message = models.CharField(
        max_length=10,
        choices=[('text', 'Text'), ('file', 'File')],
        default='text'
    )
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message de {self.auteur.username} dans la conversation {self.conversation.id}"

    class Meta:
        db_table = 'message'
        ordering = ['date_envoi']


class FichierJointMessage(models.Model):
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="fichiers_joints"
    )
    fichier = models.FileField(upload_to="messages/fichiers/")
    taille = models.IntegerField(null=True, blank=True)  # Taille en Ko
    type_fichier = models.CharField(max_length=20)  # Exemple : PDF, DOCX, etc.

    def __str__(self):
        return f"Fichier joint {self.fichier.name} pour le message {self.message.id}"

    class Meta:
        db_table = 'fichier_joint_message'


class Contract(models.Model):
    STATUT_CHOICES = [
        ('signed', 'Signé'),
        ('not_signed', 'Non signé'),
    ]

    # Relations vers Restaurant et Candidat
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='contracts')
    candidat = models.ForeignKey('Candidat', on_delete=models.CASCADE, related_name='contracts')

    # Informations sur le contrat
    date_signature = models.DateField(null=True, blank=True)  # Date de signature du contrat
    date_debut = models.DateField(null=True, blank=True)  # Date de début du contrat
    date_fin = models.DateField(null=True, blank=True)  # Date de fin du contrat
    type_contrat = models.CharField(max_length=100, null=True, blank=True,
                                    choices=[('CDI', 'CDI'), ('CDD', 'CDD')])  # Type de contrat
    salaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Salaire du candidat
    horaire_travail = models.CharField(max_length=100, null=True, blank=True, choices=[('temps_plein', 'Temps plein'), (
        'temps_partiel', 'Temps partiel')])  # Temps de travail

    # Statut du contrat (signé ou non signé)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='not_signed')

    # Autres informations spécifiques à chaque partie
    restaurant_comments = models.TextField(null=True, blank=True)  # Commentaires du restaurant sur le contrat
    candidat_comments = models.TextField(null=True, blank=True)  # Commentaires du candidat sur le contrat

    def __str__(self):
        return f"Contrat entre {self.restaurant.nom} et {self.candidat.nom}"

    class Meta:
        db_table = 'contract'
        verbose_name = 'Contrat'
        verbose_name_plural = 'Contrats'
