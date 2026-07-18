# website/models.py

from urllib.parse import urlparse, urlunparse

from django.db import models


def normalize_website_url(value):
    if not value:
        return value

    value = value.strip()
    if not value:
        return value

    if value.startswith("//"):
        value = "https:" + value
    elif "://" not in value:
        value = "https://" + value

    parsed = urlparse(value)
    scheme = "https"
    netloc = parsed.netloc
    path = parsed.path

    if not netloc and path:
        parts = path.split("/", 1)
        netloc = parts[0]
        path = f"/{parts[1]}" if len(parts) > 1 else ""

    if netloc and not netloc.startswith("www."):
        netloc = f"www.{netloc}"

    return urlunparse((scheme, netloc, path, parsed.params, parsed.query, parsed.fragment))

class Categorie(models.Model):
    designation = models.CharField(max_length=50)

class Prospect(models.Model):
    name = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    enterprise_label = models.CharField(max_length=50)
    site_web = models.URLField(max_length=200, blank=True, null=True)
    role = models.CharField(max_length=25)
    tel = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)
    
    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('annule', 'Annulé'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')
    
    TAILLE_CHOICES = [
        ('1-5', '1 à 5 employés'),
        ('6-20', '6 à 20 employés'),
        ('21-50', '21 à 50 employés'),
        ('50+', 'Plus de 50 employés'),
    ]
    
    taille_entreprise = models.CharField(
        max_length=10, 
        choices=TAILLE_CHOICES, 
        default='1-5'
    )

    def __str__(self):
        return f"{self.name} {self.lastname}"

    def save(self, *args, **kwargs):
        self.site_web = normalize_website_url(self.site_web)
        super().save(*args, **kwargs)

class Rendezvous(models.Model):
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    
    STATUT_RDV = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
        ('reporte', 'Reporté'),
        ('terminee', 'Terminé'),
    ]
    
    statut = models.CharField(max_length=20, choices=STATUT_RDV, default='en_attente')
    
    def __str__(self):
        return self.designation
    
    
class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    
    def __str__(self):
        return f"Contact from {self.name} <{self.email}>"
    
class Commentaire(models.Model):
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Commentaire by {self.prospect.name} {self.prospect.lastname} at {self.created_at}"
    
