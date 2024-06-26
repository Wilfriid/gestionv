# Generated by Django 5.0.3 on 2024-05-04 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashbord_admin', '0002_alter_vente_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenoms', models.CharField(max_length=100)),
                ('genre', models.CharField(choices=[('Masculin', 'Masculin'), ('Feminin', 'Feminin')], max_length=10)),
                ('adresse', models.TextField()),
                ('contact', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(max_length=20)),
                ('amount', models.IntegerField()),
            ],
        ),
    ]
