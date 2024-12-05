# Generated by Django 5.1.1 on 2024-12-05 00:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobfiksi_api', '0015_remove_candidat_age_alter_annonce_date_publication_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidature',
            options={'ordering': ['date_candidature'], 'verbose_name': 'Candidature', 'verbose_name_plural': 'Candidatures'},
        ),
        migrations.AddField(
            model_name='customuser',
            name='candidat',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobfiksi_api.candidat'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='restaurant',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobfiksi_api.restaurant'),
        ),
        migrations.AlterField(
            model_name='candidat',
            name='experience',
            field=models.TextField(blank=True, choices=[("Plus d'expereince", "Plus d'expereince"), ("Moins d'expereince", "Moins d'expereince"), ('plus de 1 an', 'plus de 1 an'), ('plus de 2 ans', 'plus de 2 ans'), ('plus de 5 ans', 'plus de 5 ans'), ('plus de 10 ans', 'plus de 10 ans')], max_length=255, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='candidature',
            unique_together={('candidat', 'annonce')},
        ),
    ]
