import json
import os
from django.core.management.base import BaseCommand
from jobfiksi_api.models import Ville  # Assure-toi que ce modèle existe

class Command(BaseCommand):
    help = 'Populate the Ville table with data from villes.json'

    def handle(self, *args, **kwargs):
        # Utilise le chemin absolu du fichier
        file_path = os.path.join(os.path.dirname(__file__), 'villes.json')

        with open(file_path, 'r') as file:
            villes = json.load(file)

            for ville_data in villes:
                Ville.objects.create(
                    nom=ville_data['nom'],
                    code_postal=ville_data['code_postal'],
                    # Assure-toi que ces champs correspondent à ceux de ton modèle
                )
        self.stdout.write(self.style.SUCCESS('Successfully populated villes database!'))
