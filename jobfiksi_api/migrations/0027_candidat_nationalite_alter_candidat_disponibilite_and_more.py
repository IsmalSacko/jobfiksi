# Generated by Django 5.1.1 on 2024-12-15 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobfiksi_api', '0026_candidat_niveau_etude'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidat',
            name='nationalite',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='candidat',
            name='disponibilite',
            field=models.CharField(blank=True, choices=[('tout de suite', 'Tout de suite'), ('dans 3 jours', 'Dans 3 jours'), ('dans les prochaines semaines', 'Dans les prochaines semaines'), ('dans les prochains mois', 'Dans les prochains mois')], max_length=100, null=True),
        ),
        migrations.RemoveField(
            model_name='candidat',
            name='experiences',
        ),
        migrations.RemoveField(
            model_name='candidat',
            name='formations',
        ),
        migrations.AlterField(
            model_name='candidat',
            name='langues_parlees',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='candidat',
            name='specilaite',
            field=models.CharField(blank=True, choices=[('serveur', 'Serveur'), ('cuisinier', 'Cuisinier'), ('livreur', 'Livreur'), ('nettoyage', 'Nettoyage'), ('chef', 'Chef')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='formationscandidat',
            name='niveauFormation',
            field=models.CharField(blank=True, choices=[('bac', 'Bac'), ('bac+2', 'Bac+2'), ('bac+3', 'Bac+3'), ('bac+5', 'Bac+5'), ('autre', 'Autre')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='candidat',
            name='experiences',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='candidat',
            name='formations',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
