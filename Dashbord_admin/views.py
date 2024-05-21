from itertools import count
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View , TemplateView
import plotly
from .form import ClientForm, CustomUserCreationForm, VendeurUpdateForm, VenteForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import CustomUserCreationForm
import csv
from .form import UploadFileForm
import pandas as pd
from .models import Stock, VendeurProfile, Vente, Vendeur, CategorieProduit, Produit, Client,Utilisateur
from .models import Sale
import json
from django.db.models import Sum
from django.shortcuts import render
from .models import Client, Vente
from .form import VenteForm
from .form import VendeurProfileForm
from django.contrib.messages import constants as messages_constants
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
from django.db.models.functions import ExtractMonth, ExtractYear
import plotly.graph_objs as go
import plotly.express as px


# Create your views here.


def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'connexion.html')

@login_required
def dashbord(request):
    """retouner le dashbord"""
    return render(request, 'index.html')

def deconnexion(request):
    logout(request)
    return redirect('connexion')

#Inscription
def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('connexion')
    else:
        form = CustomUserCreationForm()
    return render(request, 'inscription.html', {'form': form})

###
def handle_uploaded_file(file, user_id):
    # IdVendeur=request.user.id
    if file.name.endswith('.csv'):
        data = pd.read_csv(file, sep=";")
    elif file.name.endswith('.xlsx'):
        data = pd.read_excel(file)
    else:
        raise ValueError("Le fichier n'est pas un format supporté. Seuls CSV et Excel sont acceptés.")
    
    df=data.copy()   
    for index, row in df.iterrows():
        # Split le nom pour obtenir prenoms et nom
        name_parts = row['Name'].split(' ', 1)
        prenoms = name_parts[0]
        Nom = name_parts[1] if len(name_parts) > 1 else ''  # Gère les noms sans prénom

        # Créer ou récupérer le client
        client_instance, created = Client.objects.get_or_create(
            prenoms=prenoms, 
            Nom=Nom, 
            defaults={'Gender': row['Gender']}
        )
        
        vendeur_instance = Vendeur.objects.get(id=user_id)
        # Créer ou récupérer la catégorie de produit
        categorie, _ = CategorieProduit.objects.get_or_create(Nom=row['Type'])
        
        # Créer ou récupérer le produit
        produit, created_produit = Produit.objects.get_or_create(
        Nom=row['Produit'],
        PrixUnitaire=row['Prix'],
        IdCategorieProduit=categorie
)

        stock, created_stock = Stock.objects.get_or_create(
            IdProduit=produit,
            Quantite=250,
        )
        
         # Créer la vente si le produit, le client et la catégorie n'existent pas déjà
        
        Vente.objects.create(
            IdVendeur=vendeur_instance,  # Vous devez définir l'ID du vendeur approprié
            IdClient=client_instance,
            IdProduit=produit,
            Quantite=1,  # Vous devez définir la quantité vendue appropriée
            Montant=row['Prix'],
            Date=row['Date']
        )


@login_required(login_url='connexion')
@login_required(login_url='connexion')
def vente(request):
    user = request.user.id
    try:
        vendeur = Vendeur.objects.get(IdUtilisateur=user)
    except Vendeur.DoesNotExist:
        return redirect('index')
    # form = UploadFileForm(request.POST, request.FILES)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        
        if form.is_valid():
            file = request.FILES['file']
            if file.name.endswith('.csv'):
                # Traitement du fichier CSV avec Pandas
                handle_uploaded_file(file, vendeur.id_Vendeur)
                messages.success(request, "Vente enregistrée avec succès.")
                return render(request, 'vente.html', {'form': form})

            elif file.name.endswith(('.xlsx', '.xls')):
                # Traitement du fichier Excel avec Pandas
                handle_uploaded_file(file, vendeur.id_Vendeur)
                messages.success(request, "Vente enregistrée avec succès.")
                return render(request, 'vente.html', {'form': form})

            else:
                messages.warning(request, 'Le fichier doit être au format CSV ou excel')
    else:
        form = UploadFileForm() 
    # Filtrer les ventes en fonction du vendeur
    ventes = Vente.objects.filter(IdVendeur=vendeur.id_Vendeur).select_related( 'IdProduit__IdCategorie')
    nombre_total_ventes = ventes.count()
    paginator = Paginator(ventes, 25)  # Affiche 25 ventes par page
    page_number = request.GET.get('page')
    ventes = paginator.get_page(page_number)
    ventes = Vente.objects.all()  # Récupère toutes les ventes de la base de données

   
 

    context = {
        'vente':ventes,
        'form' :form,
        
        'nombre_total_ventes': nombre_total_ventes  # Ajoutez cette ligne pour inclure le nombre total de ventes dans le contexte

    }


    
    return render(request, 'vente.html', {'form': form, 'ventes':ventes, 'nombre_total_ventes':nombre_total_ventes})


   


@login_required
def produit(request):
    produits = Produit.objects.all()
    produits_count = produits.count()  # Utilisation de la méthode count() pour obtenir le nombre de produits
    context = {
        'produits': produits,
        'produits_count': produits_count
    }
    return render(request, 'produit.html', context)


@login_required
def client(request):
    clients = Client.objects.all()
    clients_count = clients.count()
    context = {
        'clients': clients,
        'clients_count': clients_count
    }
    return render(request, 'client.html', context)


@login_required
def stock(request):
    stocks = Stock.objects.all()
    return render(request, 'stock.html', {'stocks': stocks})

@login_required
def categorieproduit(request):
    categorieproduits = CategorieProduit.objects.all()
    return render(request, 'catéproduit.html', {'categorieproduits': categorieproduits})



def acceuil(request):
    return render(request, 'acceuil.html')


@login_required
# def ajoutvente(request):
    
#     if request.method == 'POST':
#         form_vente =VenteForm(request.POST)
#         if form_vente.is_valid():
#             form_vente.save()
#             return redirect('vente')
#     else:
#         form_vente =VenteForm()
#     return render(request, 'ajoutvente.html', locals())




def ajoutvente(request):
    if request.method == 'POST':
        form_vente = VenteForm(request.POST)
        if form_vente.is_valid():
            form_vente.save()
            # Ajout d'un message de succès
            messages.success(request, "La vente a été ajoutée avec succès.")
            return redirect('vente')  # Rediriger vers la vue de liste des ventes
    else:
        form_vente = VenteForm()
    return render(request, 'ajoutvente.html', {'form_vente': form_vente})


@login_required
def suppr(request, vente_id):
    vente = get_object_or_404(Vente, id=vente_id)
    vente.delete()
    return redirect('vente') # Redirigez l'utilisateur vers une autre page après la suppression
    


@login_required
def modifvente(request, vente_id):
    vente = get_object_or_404(Vente, id=vente_id)
    if request.method == 'POST':
        form = VenteForm(request.POST, instance=vente)
        if form.is_valid():
            form.save()
            return redirect('vente')  # Rediriger vers la liste des ventes après la modification
    else:
        form = VenteForm(instance=vente)
    return render(request, 'modifvente.html', {'form': form, 'vente': vente})


















@login_required
def ajclient(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            client_Nom = form.cleaned_data.get('Nom')
            messages.success(request, f'{client_Nom} a été ajouté avec succès')
            
            # Définir l'expiration du message à 10 secondes
            request.session.set_expiry(timezone.now() + timedelta(seconds=10))

            
            return redirect('client')  # Redirigez vers une vue de liste de clients par exemple
    else:
        form = ClientForm()
        
    # Récupérer le message de succès
    success_message = None
    for message in messages.get_messages(request):
        if message.tags == messages.SUCCESS:
            success_message = message.message
            
    return render(request, 'ajclient.html', {'form': form, 'success_message': success_message})


@login_required
def modifclient(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client')  # Rediriger vers la liste des clients après la modification
    else:
        form = ClientForm(instance=client)
    return render(request, 'modifclient.html', {'form': form, 'client': client})

@login_required
def supclient(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    client.delete()
    return redirect('client')  





def pprofilevendeur(request):
    vendeur_profile = VendeurProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = VendeurProfileForm(request.POST, request.FILES, instance=vendeur_profile)
        if form.is_valid():
            form.save()
            return redirect('pprofilevendeur')
    else:
        form = VendeurProfileForm(instance=vendeur_profile)
    return render(request, 'pprofilevendeur.html', {'form': form})


# def vendeur(request):
#     # Supposons que vous récupérez les données du vendeur de la base de données ici
#     vendeur = Vendeur.objects.get(id_Vendeur=1)
#     return render(request, 'vendeur.html', {'vendeur': vendeur})


def vendeur(request):
    if request.user.is_authenticated:
        try:
            vendeur = Vendeur.objects.get(IdUtilisateur_id=request.user.id)
            context = {'vendeur': vendeur}
            return render(request, 'vendeur.html', context)
        except Vendeur.DoesNotExist:
            return HttpResponse("Pas de profil de vendeur correspondant trouvé.")
    else:
        return HttpResponse("You are not authenticated")


# def modifvendeur(request, id_vendeur):
#     vendeur = get_object_or_404(Vendeur, id_Vendeur=id_vendeur)
#     if request.method == 'POST':
#         form = VendeurProfileForm(request.POST, instance=vendeur)
#         if form.is_valid():
#             form.save()
#             return redirect('vendeur', id_vendeur=id_vendeur)
#     else:
#         form = VendeurProfileForm(instance=vendeur)
#     return render(request, 'modifvendeur.html', {'form': form})



# graphique
# def dashbord(request):
#     # Chiffre d'affaires par année
#     ventes_par_annee = (Vente.objects
#                             .annotate(year=TruncYear('Date'))
#                             .values('year')
#                             .annotate(chiffre_affaire=Sum('Montant'))
#                             .order_by('year'))
#     # Chiffre d'affaires par mois
#     ventes_par_mois = (Vente.objects
#                           .annotate(month=TruncMonth('Date'))
#                           .values('month')
#                           .annotate(chiffre_affaire=Sum('Montant'))
#                           .order_by('month'))
#     # Top 5 clients
#     top_clients = (Client.objects
#                        .annotate(total_achats=Sum('vente__Montant'))
#                        .order_by('-total_achats')[:5])
#     # Top produits
#     top_produits = (Produit.objects
#                         .annotate(total_ventes=Sum('vente__Quantite'))
#                         .order_by('-total_ventes')[:5])
#     return render(request, 'dashbord.html', {
#         'ventes_par_annee': ventes_par_annee,
#         'ventes_par_mois': ventes_par_mois,
#         'top_clients': top_clients,
#         'top_produits': top_produits,
#     })
