from .models import Produit, Client,Vente,Stock
from .models import VendeurProfile
from .models import Vendeur
def count_objects(request):
    return {
        'total_produits': Produit.objects.count(),
        'total_clients': Client.objects.count(),
        'total_ventes': Vente.objects.count(),
        'total_stocks': Stock.objects.count(),
        
        # Ajoutez d'autres modèles si nécessaire
    }

    



def vendeur_context(request):
    try:
        vendeur = Vendeur.objects.get(IdUtilisateur_id=request.user.id)
        return {'vendeur': vendeur}
    except Vendeur.DoesNotExist:
        return {'vendeur': None}