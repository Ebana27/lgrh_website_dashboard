from django.contrib import admin

from .models import (Rendezvous, Prospect, Categorie, Contact, Commentaire)

admin.site.register(Rendezvous, list_display=['designation', 'date_time', 'statut', 'prospect'], list_filter=['statut', 'date_time'])
admin.site.register(Prospect, list_display=['name', 'lastname', 'email'], list_filter=['name', 'lastname'])
admin.site.register(Categorie, list_display=['designation'], list_filter=['designation'])
admin.site.register(Contact, list_display=['name', 'email'], list_filter=['name'])
admin.site.register(Commentaire, list_display=['prospect', 'content', 'created_at'], list_filter=['created_at'])