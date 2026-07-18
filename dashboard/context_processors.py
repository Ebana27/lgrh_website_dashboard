from website.models import Rendezvous


def dashboard_notifications(request):
    return {
        "pending_rdv_count": Rendezvous.objects.filter(statut="en_attente").count(),
    }
