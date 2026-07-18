from django.urls import path
from . import views

app_name = 'dashboard'  # IMPORTANT : Ajoutez ceci pour que dashboard:valider_rdv fonctionne

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('analytics/', views.analytics, name='analytics'),
    path('prospects/', views.prospects, name='prospects'),
    path('settings/', views.settings, name='settings'),
    path('meet/', views.meet, name='meet'),
    path('comments/', views.comments, name='comments'),
    path('messages/', views.messages, name='messages'),
    path('valider/<int:rdv_id>/', views.valider_rdv, name='valider_rdv'),
    path('annuler/<int:rdv_id>/', views.annuler_rdv, name='annuler_rdv'),
    path('reporter/<int:rdv_id>/', views.reporter_rdv, name='reporter_rdv'),
    path('search/', views.search, name='search'),
]
