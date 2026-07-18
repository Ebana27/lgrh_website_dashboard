# website/views
from django.shortcuts import redirect, render, get_object_or_404
from .models import Prospect, Rendezvous, Categorie, Contact, Commentaire
from .services.email_service import EmailService
from django.utils.dateparse import parse_datetime
from django.utils import timezone


def parse_local_datetime(value):
    parsed = parse_datetime(value)
    if not parsed:
        return None
    if timezone.is_naive(parsed):
        parsed = timezone.make_aware(parsed, timezone.get_current_timezone())
    return parsed


def home(request):
    comments = Commentaire.objects.select_related("prospect").order_by("-created_at")[:10]
    return render(request, "index.html", {"comments": comments})


def comments(request):
    if request.method == "POST":
        name = request.POST.get("name")
        lastname = request.POST.get("lastname")
        enterprise_label = request.POST.get("enterprise_label")
        role = request.POST.get("role")
        email = request.POST.get("email")
        content = request.POST.get("content")

        if name and lastname and enterprise_label and role and email and content:
            prospect = Prospect.objects.create(
                name=name,
                lastname=lastname,
                enterprise_label=enterprise_label,
                role=role,
                email=email,
                site_web=request.POST.get("site_web", ""),
                tel=request.POST.get("tel", ""),
            )
            Commentaire.objects.create(prospect=prospect, content=content)
            return redirect("comments")

    comments = Commentaire.objects.select_related("prospect").order_by("-created_at")[:10]
    return render(request, "comments.html", {"comments": comments})


def func(request):
    return render(request, "func.html")


def successprospect(request, prospect_id):
    prospect = get_object_or_404(
        Prospect,
        id=prospect_id
    )

    return render(
        request,
        "successprospect.html",
        {"p": prospect}
    )


def demo(request):
    categories = Categorie.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        lastname = request.POST.get("lastname")
        enterprise = request.POST.get("enterprise_label")
        role = request.POST.get("role")

        designation = request.POST.get("designation")
        date_time_str = request.POST.get("date_time")
        categorie_id = request.POST.get("categorie") or None
        taille_entreprise = request.POST.get("taille_entreprise") or "1-5"
        tel = request.POST.get("tel", "").strip()

        categorie = None
        if categorie_id:
            categorie = Categorie.objects.filter(id=categorie_id).first()

        if name and lastname and enterprise and role and designation and date_time_str:
            nouveau_prospect = Prospect.objects.create(
                name=name,
                lastname=lastname,
                enterprise_label=enterprise,
                site_web=request.POST.get("site_web", ""),
                role=role,
                tel=tel,
                email=request.POST.get("email", ""),
                categorie=categorie,
                taille_entreprise=taille_entreprise,
            )

            nouveau_rendezvous = Rendezvous.objects.create(
                prospect=nouveau_prospect,
                designation=designation,
                date_time=parse_local_datetime(date_time_str),
                statut="en_attente"
            )

            EmailService.notify_owner_of_demo_request(nouveau_prospect, nouveau_rendezvous)

            return redirect("successprospect", nouveau_prospect.id)

    return render(request, "demo.html", {"categories": categories})


def successprospect_noid(request):
    """Fallback view when no prospect_id is provided: redirect to home."""
    return redirect("home")


def contact_success(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    return render(request, "contact_success.html", {"name": contact.name, "contact_id": contact.id})


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if name and email and message:
            contact = Contact.objects.create(name=name, email=email, message=message)
            EmailService.notify_owner_of_contact_message(contact)

            return redirect("contact_success", contact.id)
    return render(request, "contact.html")
