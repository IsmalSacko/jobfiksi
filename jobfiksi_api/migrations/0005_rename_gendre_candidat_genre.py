# Generated by Django 5.1.1 on 2024-11-15 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobfiksi_api', '0004_alter_candidat_nom_alter_candidat_prenom'),
    ]

    operations = [
        migrations.RenameField(
            model_name='candidat',
            old_name='gendre',
            new_name='genre',
        ),
    ]
