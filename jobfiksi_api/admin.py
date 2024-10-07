# admin.py
from django.contrib import admin
from .models import CustomUser, Offre, Ville  # N'oubliez pas d'importer le modèle Ville

class VilleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code_postal')  # Ajoutez le code postal à la liste d'affichage
    search_fields = ('nom', 'code_postal')  # Ajoutez le code postal à la barre de recherche

admin.site.register(Ville, VilleAdmin)  # Enregistrez le modèle Ville dans l'administration

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type')
    search_fields = ('username', 'email', 'user_type')

admin.site.register(CustomUser, CustomUserAdmin)

class OffreAdmin(admin.ModelAdmin):
    list_display = ('titre', 'description', 'salaire', 'localisation', 'date_creation', 'user')
    search_fields = ('titre', 'description', 'salaire', 'localisation__nom', 'date_creation', 'user__username')  # Utilisez la relation pour chercher par nom

admin.site.register(Offre, OffreAdmin)
