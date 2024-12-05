from django.contrib import admin
from .models import CustomUser, Candidat, Restaurant, Annonce, Candidature


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
    list_display = ('nom', 'prenom', 'tel', 'date_naissance', 'cv', 'niveau_etude', 'experience')
    search_fields = ('nom', 'prenom', 'tel')
    list_filter = ('date_naissance',)


# Personnalisation de l'affichage du Restaurant dans l'admin
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('nom', 'tel', 'user')
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


# Enregistrement des modèles avec les personnalisations

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Candidat, CandidatAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Annonce, AnnonceAdmin)
admin.site.register(Candidature, CandidatureAdmin)
