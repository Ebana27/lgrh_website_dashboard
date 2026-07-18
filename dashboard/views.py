import json
from functools import wraps
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages as django_messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_datetime
from website.models import Rendezvous, Prospect, Contact, Commentaire
from .services.email_service import EmailService
from django.db.models import Q


def staff_required(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated or not user.is_staff:
            return redirect_to_login(request.get_full_path())
        return view_func(request, *args, **kwargs)

    return wrapped


@staff_required
def dashboard_home(request):
    rdv_attente = (
        Rendezvous.objects
        .filter(statut='en_attente')
        .select_related('prospect')
        .order_by('-date_time')
    )
    recent_rdvs = Rendezvous.objects.select_related('prospect').order_by('-date_time')[:6]
    context = {
        'rdv_attente': rdv_attente,
        'recent_rdvs': recent_rdvs,
        'total_prospects': Prospect.objects.count(),
        'total_messages': Contact.objects.count(),
        'total_comments': Commentaire.objects.count(),
        'active_page': 'home',
    }
    return render(request, 'dashboard/index.html', context)

@staff_required
def analytics(request):
    # Compteurs globaux
    rdv_count = Rendezvous.objects.filter(statut='en_attente').count()
    total_prospects = Prospect.objects.count()
    total_messages = Contact.objects.count()
    total_comments = Commentaire.objects.count()

    # --- DONNÉES POUR LES GRAPHIQUES ---
    # 1. Répartition des Prospects par statut
    prospects_data = {
        'en_attente': Prospect.objects.filter(status='en_attente').count(),
        'valide': Prospect.objects.filter(status='valide').count(),
        'annule': Prospect.objects.filter(status='annule').count(),
    }

    # 2. Répartition des Rendez-vous par statut
    rdv_data = {
        'en_attente': Rendezvous.objects.filter(statut='en_attente').count(),
        'confirme': Rendezvous.objects.filter(statut='confirme').count(),
        'annule': Rendezvous.objects.filter(statut='annule').count(),
        'reporte': Rendezvous.objects.filter(statut='reporte').count(),
        'terminee': Rendezvous.objects.filter(statut='terminee').count(),
    }

    # Listes pour le bas de page
    upcoming_rdvs = Rendezvous.objects.filter(statut__in=['en_attente', 'confirme']).select_related('prospect').order_by('-date_time')[:5]
    recent_comments = Commentaire.objects.select_related('prospect').order_by('-created_at')[:5]

    context = {
        'rdv_count': rdv_count,
        'total_prospects': total_prospects,
        'total_messages': total_messages,
        'total_comments': total_comments,
        'upcoming_rdvs': upcoming_rdvs,
        'recent_comments': recent_comments,
        # Conversion en JSON pour JavaScript
        'prospects_chart_data': json.dumps(prospects_data),
        'rdv_chart_data': json.dumps(rdv_data),
        'active_page': 'analytics',
    }
    return render(request, 'dashboard/analytics.html', context)


@staff_required
def prospects(request):
    prospects = Prospect.objects.order_by('-id')[:20]
    context = {
        'prospects': prospects,
        'active_page': 'prospects',
    }
    return render(request, 'dashboard/prospects.html', context)


@staff_required
def settings(request):
    form = PasswordChangeForm(request.user)

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            django_messages.success(request, "Votre mot de passe a été mis à jour.")
            return redirect('dashboard:settings')
        django_messages.error(request, "Le mot de passe n'a pas pu être mis à jour. Vérifiez les champs.")

    context = {
        'active_page': 'settings',
        'password_form': form,
    }
    return render(request, 'dashboard/settings.html', context)


@staff_required
def valider_rdv(request, rdv_id):
    if request.method == "POST":
        rdv = get_object_or_404(Rendezvous, id=rdv_id)
        EmailService.confirmation(rdv)
        rdv.statut = 'confirme'
        rdv.save()

    return redirect('dashboard:home')

@staff_required
def annuler_rdv(request, rdv_id):
    if request.method == "POST":
        rdv = get_object_or_404(Rendezvous, id=rdv_id)
        rdv.statut = 'annule'
        rdv.save()
        EmailService.Annulation(rdv)
    return redirect('dashboard:home')

@staff_required
def reporter_rdv(request, rdv_id):
    if request.method == "POST":
        rdv = get_object_or_404(Rendezvous, id=rdv_id)
        new_date_time = request.POST.get('new_date_time')
        choice = request.POST.get('reschedule_choice')
        if new_date_time:
            parsed = parse_datetime(new_date_time)
            if parsed:
                rdv.date_time = parsed
        rdv.statut = 'reporte'
        rdv.save()
        EmailService.Reporter(rdv, choice=choice, new_date_time=rdv.date_time if new_date_time else None)

    return redirect('dashboard:home')

@staff_required
def meet(request):
    rdv_list = Rendezvous.objects.select_related('prospect').order_by('-date_time')
    context = {
        'rdv_list': rdv_list,
        'active_page': 'meet',
    }
    rdv_designations = [rdv.designation for rdv in rdv_list]
    context['rdv_designations'] = rdv_designations
    return render(request, 'dashboard/meet.html', context)

@staff_required
def comments(request):
    comment = Commentaire.objects.order_by('-id')[:20]
    context = {
        'active_page': 'comments',
        'comments': comment,
    }
    return render(request, 'dashboard/comments.html', context)

# Un message est un message envoyé par un utilisateur via le formulaire de contact. Il contient le nom, l'email et le contenu du message. et est affiché dans la page messages du dashboard. Il est possible de supprimer un message depuis le dashboard.
@staff_required
def messages(request):
    messages = Contact.objects.order_by('-id')[:20]
    context = {
        'active_page': 'messages',
        'messages': messages,
    }
    return render(request, 'dashboard/messages.html', context)


@staff_required
def search(request):
    q = request.GET.get('q', '').strip()
    prospects = Prospect.objects.none()
    rdvs = Rendezvous.objects.none()
    if q:
        prospects = Prospect.objects.filter(
            Q(name__icontains=q) | Q(lastname__icontains=q) | Q(enterprise_label__icontains=q) | Q(email__icontains=q)
        ).order_by('-id')[:50]

        rdvs = Rendezvous.objects.filter(
            Q(prospect__name__icontains=q) | Q(prospect__lastname__icontains=q) | Q(designation__icontains=q)
        ).select_related('prospect').order_by('-date_time')[:50]

    context = {
        'q': q,
        'prospects': prospects,
        'rdv_results': rdvs,
        'active_page': 'prospects' if prospects.exists() else 'home',
    }
    return render(request, 'dashboard/search.html', context)

@staff_required
def delete_message(request, message_id):
    if request.method == "POST":
        message = get_object_or_404(Contact, id=message_id)
        message.delete()
    return redirect('dashboard:messages')

@staff_required
def setting(request, setting_id):
    # Placeholder for future settings functionality
    return redirect('dashboard:settings')
