# Generated by Django 5.1.1 on 2024-12-11 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobfiksi_api', '0022_rename_ad_cv_candidature_cv_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FichierJoint',
            new_name='FichierJointMessage',
        ),
        migrations.AlterModelTable(
            name='entretien',
            table='entretien',
        ),
        migrations.AlterModelTable(
            name='fichierjointmessage',
            table='fichier_joint_message',
        ),
    ]