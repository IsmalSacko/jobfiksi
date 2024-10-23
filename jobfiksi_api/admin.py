from django.contrib import admin
from .models import Ville, CustomUser, Candidat, Restaurant, Annonce, Candidature, PreferenceCandidat, PreferenceRestaurant, Offre

# Enregistrement du modèle Ville
@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code_postal')  # Afficher le nom et le code postal dans la liste
    search_fields = ('nom', 'code_postal')  # Ajouter une barre de recherche

# Enregistrement du modèle CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_superuser', 'is_active')  # Afficher ces champs dans la liste
    list_filter = ('user_type', 'is_staff', 'is_active')  # Ajouter des filtres sur ces champs
    search_fields = ('username', 'email')  # Ajouter une barre de recherche

# Enregistrement du modèle Candidat
@admin.register(Candidat)
class CandidatAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'tel', 'ville')  # Afficher ces champs dans la liste
    search_fields = ('nom', 'prenom', 'tel', 'adresse')  # Ajouter une barre de recherche
    list_filter = ('ville',)  # Ajouter un filtre sur la ville

# Enregistrement du modèle Restaurant
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('nom', 'tel', 'ville', 'type')  # Afficher ces champs dans la liste
    search_fields = ('nom', 'tel', 'adresse')  # Ajouter une barre de recherche
    list_filter = ('ville', 'type')  # Ajouter des filtres sur la ville et le type de restaurant

# Enregistrement du modèle Annonce
@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_contrat', 'temps_travail', 'statut', 'created_by', 'date_publication')  # Afficher ces champs
    list_filter = ('type_contrat', 'temps_travail', 'statut', 'date_publication')  # Ajouter des filtres
    search_fields = ('titre', 'description')  # Ajouter une barre de recherche

# Enregistrement du modèle Candidature
@admin.register(Candidature)
class CandidatureAdmin(admin.ModelAdmin):
    list_display = ('candidat', 'annonce', 'date_candidature')  # Afficher ces champs
    list_filter = ('date_candidature',)  # Ajouter un filtre sur la date de candidature
    search_fields = ('candidat__nom', 'annonce__titre')  # Ajouter une barre de recherche

# Enregistrement du modèle PreferenceCandidat
@admin.register(PreferenceCandidat)
class PreferenceCandidatAdmin(admin.ModelAdmin):
    list_display = ('candidat', 'secteur', 'type_contrat', 'horaire_travail')  # Afficher ces champs
    list_filter = ('type_contrat', 'flexibilite_deplacement')  # Ajouter des filtres
    search_fields = ('candidat__nom', 'secteur')  # Ajouter une barre de recherche

# Enregistrement du modèle PreferenceRestaurant
@admin.register(PreferenceRestaurant)
class PreferenceRestaurantAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'niveau_etude', 'horaire_travail', 'possibilite_former')  # Afficher ces champs
    list_filter = ('niveau_etude', 'possibilite_former', 'possibilite_debutant')  # Ajouter des filtres
    search_fields = ('restaurant__nom',)  # Ajouter une barre de recherche

# Enregistrement du modèle Offre
@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = ('annonce',)  # Afficher le titre de l'annonce liée
    search_fields = ('annonce__titre',)  # Ajouter une barre de recherche

