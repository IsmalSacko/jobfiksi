from django.contrib import admin
from .models import Adresse, CustomUser, Candidat, Restaurant, Annonce, Candidature, PreferenceCandidat, PreferenceRestaurant, Offre

# Personnalisation de l'affichage de l'adresse dans l'admin
class AdresseAdmin(admin.ModelAdmin):
    list_display = ('rue', 'ville', 'code_postal', 'pays', 'created_by')
    search_fields = ('rue', 'ville', 'code_postal', 'pays')

# Personnalisation de l'affichage du CustomUser dans l'admin
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_active', 'is_staff')
    search_fields = ('username', 'email')

# Personnalisation de l'affichage du Candidat dans l'admin
class CandidatAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'tel', 'date_naissance', 'adresse', 'cv', 'niveau_etude', 'experience')
    search_fields = ('nom', 'prenom', 'tel')
    list_filter = ('date_naissance',)

# Personnalisation de l'affichage du Restaurant dans l'admin
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('nom', 'tel', 'adresse', 'user')
    search_fields = ('nom', 'tel')

# Personnalisation de l'affichage de l'Annonce dans l'admin
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_contrat', 'salaire', 'temps_travail', 'statut', 'created_by', 'date_publication')
    search_fields = ('titre', 'description')
    list_filter = ('type_contrat', 'temps_travail', 'statut')

# Personnalisation de l'affichage de la Candidature dans l'admin
class CandidatureAdmin(admin.ModelAdmin):
    list_display = ('candidat', 'annonce', 'date_candidature')
    search_fields = ('candidat__nom', 'annonce__titre')

# Personnalisation de l'affichage de la PreferenceCandidat dans l'admin
class PreferenceCandidatAdmin(admin.ModelAdmin):
    list_display = ('candidat', 'secteur', 'type_contrat', 'type_restaurant', 'horaire_travail')
    search_fields = ('candidat__nom', 'secteur')

# Personnalisation de l'affichage de la PreferenceRestaurant dans l'admin
class PreferenceRestaurantAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'niveau_etude', 'possibilite_former', 'horaire_travail')
    search_fields = ('restaurant__nom', 'niveau_etude')

# Personnalisation de l'affichage de l'Offre dans l'admin
class OffreAdmin(admin.ModelAdmin):
    list_display = ('annonce',)
    search_fields = ('annonce__titre',)

# Enregistrement des modèles avec les personnalisations
admin.site.register(Adresse, AdresseAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Candidat, CandidatAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Annonce, AnnonceAdmin)
admin.site.register(Candidature, CandidatureAdmin)
admin.site.register(PreferenceCandidat, PreferenceCandidatAdmin)
admin.site.register(PreferenceRestaurant, PreferenceRestaurantAdmin)
admin.site.register(Offre, OffreAdmin)
