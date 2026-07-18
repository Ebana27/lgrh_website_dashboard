"""
URL configuration for green project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from website import views
from django.conf import settings
from django.conf.urls.static import static
from .views import custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('', views.home, name='home'),
    path('demo/', views.demo, name='demo'),
    path('comments/', views.comments, name='comments'),
    path('contact/', views.contact, name='contact'),
    path('successprospect/', views.successprospect_noid, name='successprospect_noid'),
    path('successprospect/<int:prospect_id>/', views.successprospect, name='successprospect'),
    path('contactsuccess/<int:contact_id>/', views.contact_success, name='contact_success'),
    
    # Appliquer la page 404 spéciale pour les pages non trouvées
    path('404/', custom_404, name='custom_404'),

    # URL pour le dashboard
    path('dashboard/', include('dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'green.views.custom_404'