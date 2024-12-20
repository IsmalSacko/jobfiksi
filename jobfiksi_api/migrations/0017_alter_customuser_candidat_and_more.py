# Generated by Django 5.1.1 on 2024-12-05 00:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobfiksi_api', '0016_alter_candidature_options_customuser_candidat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='candidat',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='candidat', to='jobfiksi_api.candidat'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='restaurant',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to='jobfiksi_api.restaurant'),
        ),
    ]
