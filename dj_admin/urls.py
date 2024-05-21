
from django.urls import path, include
from django.contrib import admin
from Dashbord_admin import views
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
    path('', views.dashbord, name='dashbord'),
    path('admin/', admin.site.urls),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('index/', views.dashbord, name='index'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('vente/', views.vente, name='vente'),
    path('suppr/<int:vente_id>/', views.suppr, name='suppr'),
    path('modifvente/<int:vente_id>/', views.modifvente, name='modifvente'),
    # path('confirmation/<int:pk>/', views.confirmation, name='confirmation'),
    path('produit/', views.produit, name='produit'),
    path('client/', views.client, name='client'),
    path('stock/', views.stock, name='stock'),
    path('categorieproduit/', views.categorieproduit, name='categorieproduit'),
    path('ajoutvente/', views.ajoutvente, name='ajoutvente'),
    path('acceuil/', views.acceuil, name='acceuil'),
    path('ajclient/', views.ajclient, name='ajclient'),
    path('modifclient/<int:client_id>/', views.modifclient, name='modifclient'),
    path('supclient/<int:client_id>/', views.supclient, name='supclient'),
    # path('statistique/', views.statistique, name='statistique'),
    # path('dashbord/', views.dashbord, name='dashbord'),
    
    path('pprofilevendeur/', views.pprofilevendeur, name='pprofilevendeur'),
    path('vendeur/', views.vendeur, name='vendeur'),
    # path('modifvendeur/<int:id_vendeur>/', views.modifvendeur, name='modifvendeur'),
    
   
]  

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)