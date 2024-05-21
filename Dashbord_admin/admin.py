from django.contrib import admin
from .models import Client, Utilisateur, Vendeur, Admin, CategorieProduit, Produit, Stock, Vente

# Register your models here.

admin.site.register(Client)
admin.site.register(Utilisateur)
admin.site.register(Vendeur)
admin.site.register(Admin)
admin.site.register(CategorieProduit)
admin.site.register(Produit)
admin.site.register(Stock)
admin.site.register(Vente)

