from django.conf import settings
from django.core.mail import EmailMessage
from smtplib import SMTPException
import logging
from email.utils import parseaddr

logger = logging.getLogger(__name__)


class EmailService:

    @staticmethod
    def get_owner_email():
        _, owner_email = parseaddr(getattr(settings, 'SITE_OWNER_EMAIL', settings.DEFAULT_FROM_EMAIL))
        return owner_email

    @staticmethod
    def notify_owner_of_demo_request(prospect, rendezvous):
        owner_email = EmailService.get_owner_email()
        if not owner_email:
            return

        subject = 'Nouvelle demande de démonstration'
        date_time_str = rendezvous.date_time.strftime('%d/%m/%Y %H:%M')

        message = f"""
Bonjour,

Une nouvelle demande de démonstration a été soumise depuis le site web.

Prospect:
- Nom : {prospect.name} {prospect.lastname}
- Email : {prospect.email}
- Téléphone : {prospect.tel or 'Non renseigné'}
- Entreprise : {prospect.enterprise_label}
- Rôle : {prospect.role}

Détails du rendez-vous :
- Objet : {rendezvous.designation}
- Date et heure : {date_time_str}

Merci.
"""

        try:
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[owner_email],
                reply_to=[prospect.email] if prospect.email else None,
            )
            email.send(fail_silently=False)
        except SMTPException:
            logger.exception("Unable to send demo notification email")

    @staticmethod
    def notify_owner_of_contact_message(contact):
        owner_email = EmailService.get_owner_email()
        if not owner_email:
            return

        subject = "Nouveau message de contact"
        message = f"""
Bonjour,

Un nouveau message a été envoyé depuis le formulaire de contact.

Nom : {contact.name}
Email : {contact.email}

Message :
{contact.message}

Merci.
"""

        try:
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[owner_email],
                reply_to=[contact.email] if contact.email else None,
            )
            email.send(fail_silently=False)
        except SMTPException:
            logger.exception("Unable to send contact notification email")
