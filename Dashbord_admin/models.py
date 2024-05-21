from typing import Any
from django import forms
from django.db import models 
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser # type: ignore



# Create your models here.


class Client(models.Model):
    Nom = models.CharField(max_length=30)
    prenoms = models.CharField(max_length=100)
    Gender = models.CharField(max_length=10)
    adresse = models.CharField(max_length=100, null=True)
    contact = models.IntegerField(null=True)


    def __str__(self):
        return f"{self.Nom} {self.prenoms}"


class Utilisateur(AbstractBaseUser):
    Email = models.CharField(max_length=50, unique=True, null=False)
    username = models.CharField(max_length=50, null=True, blank=True)
    Roles = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
    
class Vendeur(models.Model):
    Nom = models.CharField(max_length=30)
    Prenoms = models.CharField(max_length=100)
    Telephone = models.IntegerField()
    IdUtilisateur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE)  # utilisez une chaîne au lieu de la classe
    image = models.ImageField(default='default.png',
                              upload_to='profile_images')
    id_Vendeur = models.AutoField(primary_key=True)  

    def __str__(self):
        return self.Nom
    


    




class Admin(models.Model):
    Nom = models.CharField(max_length=30)
    Prenoms = models.CharField(max_length=100)
    Telephone = models.IntegerField()
    IdUtilisateur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE)  # utilisez une chaîne au lieu de la classe

    def _str_(self):
        return self.Nom
    
class CategorieProduit(models.Model):
    Nom = models.CharField(max_length=100)

    def _str_(self):
        return self.Nom
    

class Produit(models.Model):
    Nom = models.CharField(max_length=100)
    Description = models.TextField(null=True)
    PrixUnitaire = models.FloatField()
    IdCategorieProduit = models.ForeignKey(CategorieProduit, on_delete=models.CASCADE)

    def _str_(self):
        return self.Nom
class Stock(models.Model):
    IdProduit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    Quantite = models.IntegerField()
    Date = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Stock {self.IdStock}"
    

class Vente(models.Model):
    IdVendeur = models.ForeignKey(Vendeur, on_delete=models.CASCADE)
    IdClient = models.ForeignKey(Client, on_delete=models.CASCADE)
    IdProduit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    Quantite = models.IntegerField()
    Montant = models.DecimalField(max_digits=10, decimal_places=2)
    Date = models.CharField(max_length=100)
    def _str_(self):
        return f"Vente {self.IdVente}"
    



class Sale(models.Model):
    month = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sale {self.id}"


# photo de profil
class VendeurProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
 

