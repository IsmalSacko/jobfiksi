# Generated by Django 5.1.1 on 2024-12-13 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobfiksi_api', '0024_remove_annonce_user_alter_annonce_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidat',
            name='preferences',
        ),
        migrations.RemoveField(
            model_name='preferencesrestaurant',
            name='restaurant',
        ),
        migrations.AddField(
            model_name='candidat',
            name='flexibilite_deplacement',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='candidat',
            name='fourchette_salaire',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='candidat',
            name='horaire_travail',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='candidat',
            name='possibilite_formation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='candidat',
            name='salaire_max',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='candidat',
            name='salaire_min',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='candidat',
            name='secteur',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='candidat',
            name='type_contrat',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='candidat',
            name='type_restaurant',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='age_min',
            field=models.IntegerField(blank=True, choices=[(18, '18'), (21, '21'), (25, '25'), (30, '30'), (35, '35'), (40, '40')], null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='attente_candidat',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='creneau_1',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='creneau_2',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='creneau_3',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='horaire_travail',
            field=models.CharField(blank=True, choices=[('matin', 'Matin'), ('midi', 'Midi'), ('soir', 'Soir'), ('nuit', 'Nuit'), ('flexible', 'Flexible')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='niveau_etude',
            field=models.CharField(blank=True, choices=[('bac', 'Bac'), ('bac+2', 'Bac+2'), ('bac+3', 'Bac+3'), ('bac+5', 'Bac+5'), ('autre', 'Autre')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='possibilite_debuter',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='possibilite_former',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='type_de_contrat',
            field=models.CharField(blank=True, choices=[('CDI', 'CDI'), ('CDD', 'CDD'), ('intérim', 'Intérim'), ('stage', 'Stage')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='type_de_travail',
            field=models.CharField(blank=True, choices=[('serveur', 'Serveur'), ('cuisinier', 'Cuisinier'), ('livreur', 'Livreur'), ('nettoyage', 'Nettoyage'), ('chef', 'Chef'), ('caissier', 'Caissier'), ('plongeur', 'Plongeur'), ('patissier', 'Patissier')], max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='PreferencesCandidat',
        ),
        migrations.DeleteModel(
            name='PreferencesRestaurant',
        ),
    ]
