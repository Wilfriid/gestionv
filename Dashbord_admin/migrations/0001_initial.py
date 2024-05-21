# Generated by Django 5.0.3 on 2024-04-17 18:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategorieProduit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=30)),
                ('prenoms', models.CharField(max_length=100)),
                ('Gender', models.CharField(max_length=10)),
                ('adresse', models.CharField(max_length=100, null=True)),
                ('contact', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('Email', models.CharField(max_length=50, unique=True)),
                ('username', models.CharField(blank=True, max_length=50, null=True)),
                ('Roles', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=100)),
                ('Description', models.TextField(null=True)),
                ('PrixUnitaire', models.FloatField()),
                ('IdCategorieProduit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashbord_admin.categorieproduit')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quantite', models.IntegerField()),
                ('Date', models.DateTimeField(auto_now_add=True)),
                ('IdProduit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashbord_admin.produit')),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=30)),
                ('Prenoms', models.CharField(max_length=100)),
                ('Telephone', models.IntegerField()),
                ('IdUtilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashbord_admin.utilisateur')),
            ],
        ),
        migrations.CreateModel(
            name='Vendeur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=30)),
                ('Prenoms', models.CharField(max_length=100)),
                ('Telephone', models.IntegerField()),
                ('IdUtilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashbord_admin.utilisateur')),
            ],
        ),
        migrations.CreateModel(
            name='Vente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quantite', models.IntegerField()),
                ('Montant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Date', models.DateTimeField(auto_now_add=True)),
                ('IdClient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashbord_admin.client')),
                ('IdProduit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashbord_admin.produit')),
                ('IdVendeur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashbord_admin.vendeur')),
            ],
        ),
    ]