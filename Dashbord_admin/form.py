
from multiprocessing.connection import Client
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import  Vendeur, Vente
from Dashbord_admin import models
from .models import Client  # Assurez-vous que l'importation du modèle est correcte
from .models import VendeurProfile


class CustomUserCreationForm(UserCreationForm):
    ROLES_CHOICES = (
        ('vendeur', 'Vendeur'),
        ('administrateur', 'Administrateur'),
        ('gestionnaire', 'Gestionnaire'),
    )

    role = forms.ChoiceField(choices=ROLES_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'password1', 'password2']


# charger le fichier
class UploadFileForm(forms.Form):
    file = forms.FileField(label='Charger un fichier de vente', widget=forms.FileInput(
            attrs= {'class':'form-control li'}),
            error_messages={'required':''})



# class Client(forms.Form):
#     nom = forms.CharField(label='Nom', max_length=100)
#     prenoms = forms.CharField(label='Prénoms', max_length=100)
#     genre = forms.ChoiceField(label='Genre', choices=[('Masculin', 'Masculin'), ('Feminin', 'Feminin')])
#     adresse = forms.CharField(label='Adresse', max_length=255)
#     contact = forms.CharField(label='Contact', max_length=20)



class Sale(forms.Form):
    month = forms.CharField(max_length=20)
    amount = forms.IntegerField()

    def __str__(self):
        return f"{self.month} - {self.amount}"
    
class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ['IdVendeur','IdClient', 'IdProduit', 'Quantite','Montant','Date']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['IdProduit'].label_from_instance = lambda obj: obj.Nom
        self.fields['IdVendeur'].label_from_instance = lambda obj: obj.Nom
        



class ClientForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('Masculin', 'Masculin'),
        ('Féminin', 'Féminin'),
    ]
    
    Gender = forms.ChoiceField(choices=GENDER_CHOICES)
    
    class Meta:
        model = Client
        fields = ['Nom', 'prenoms', 'Gender', 'adresse', 'contact']


    # photo de profile


class VendeurProfileForm(forms.ModelForm):
    class Meta:
        model = VendeurProfile
        fields = ['photo']  # Mettez à jour le nom du champ si nécessaire

class VendeurUpdateForm(forms.ModelForm):
    class Meta:
        model =  Vendeur
        fields = ['Nom', 'Prenoms','Telephone','image']