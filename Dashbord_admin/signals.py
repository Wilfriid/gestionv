from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Utilisateur, Vendeur

@receiver(post_save, sender=Utilisateur)
def create_vendeur(sender, instance, created, **kwargs):
    if created:
        Vendeur.objects.create(IdUtilisateur=instance)

@receiver(post_save, sender=Utilisateur)
def save_vendeur(sender, instance, **kwargs):
    instance.vendeur.save()  # cela nécessite que 'vendeur' soit une propriété de votre modèle Utilisateur