
# Register your models here.
from django.contrib import admin
from .models import CustomUser, Offre

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type')
    search_fields = ('username', 'email', 'user_type')

admin.site.register(CustomUser, CustomUserAdmin)

class OffreAdmin(admin.ModelAdmin):
    list_display = ('titre', 'description', 'salaire', 'localisation', 'date_creation', 'user')
    search_fields = ('titre', 'description', 'salaire', 'localisation', 'date_creation', 'user')

admin.site.register(Offre, OffreAdmin)