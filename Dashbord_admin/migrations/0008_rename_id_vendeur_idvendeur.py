# Generated by Django 5.0.3 on 2024-05-12 21:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Dashbord_admin', '0007_alter_vendeur_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vendeur',
            old_name='id',
            new_name='idVendeur',
        ),
    ]
