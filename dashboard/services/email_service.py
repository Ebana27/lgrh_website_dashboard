from django.core.mail import send_mail


class EmailService:

    @staticmethod
    def confirmation(rdv):

        sujet = "Confirmation de votre démonstration"

        date_str = rdv.date_time.strftime('%d/%m/%Y')
        heure_str = rdv.date_time.strftime('%H:%M')

        message = f"""
Bonjour {rdv.prospect.name},

Votre démonstration Green est confirmée.

Date : {date_str}

Heure : {heure_str}

Merci.
"""

        send_mail(
            sujet,
            message,
            None,
            [rdv.prospect.email],
        )

    @staticmethod
    def Annulation(rdv):

        sujet = "Annulation de votre démonstration"

        date_str = rdv.date_time.strftime('%d/%m/%Y')
        heure_str = rdv.date_time.strftime('%H:%M')

        message = f"Cher(e) {rdv.prospect.name},\n\nVotre démonstration Green prévue le {date_str} à {heure_str} a été annulée. Pour plus d'informations, veuillez nous contacter.\n\nMerci."
        send_mail(sujet, message, None, [rdv.prospect.email])
        
    @staticmethod
    def Reporter(rdv, choice=None, new_date_time=None):
        sujet = "Report de votre démonstration"

        date_str = rdv.date_time.strftime('%d/%m/%Y')
        heure_str = rdv.date_time.strftime('%H:%M')
        extra = ""
        if choice == 'prospect_choose':
            extra = "\nNous vous laissons choisir une nouvelle date qui vous convient."
        elif choice == 'new_date' and new_date_time:
            date_new = new_date_time.strftime('%d/%m/%Y')
            time_new = new_date_time.strftime('%H:%M')
            extra = f"\nLa nouvelle date proposée est le {date_new} à {time_new}."

        message = f"Cher(e) {rdv.prospect.name},\n\nVotre démonstration Green est reportée. {extra}\n\nMerci."
        send_mail(sujet, message, None, [rdv.prospect.email])