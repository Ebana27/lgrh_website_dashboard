from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from website.models import Prospect, Rendezvous
from .views import annuler_rdv


class AnnulerRdvViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.staff_user = get_user_model().objects.create_user(
            username='staff-user',
            password='password123',
            is_staff=True,
        )
        self.prospect = Prospect.objects.create(
            name='Jean',
            lastname='Dupont',
            enterprise_label='Acme',
            email='jean@example.com',
            role='Manager',
        )
        self.rdv = Rendezvous.objects.create(
            prospect=self.prospect,
            designation='Entretien',
            date_time=timezone.now(),
        )

    @patch('dashboard.views.EmailService.Annulation')
    def test_annuler_rdv_keeps_rdv_with_annule_status(self, mock_annulation):
        request = self.factory.post(f'/dashboard/rdv/{self.rdv.id}/annuler/')
        request.user = self.staff_user

        response = annuler_rdv(request, self.rdv.id)

        self.rdv.refresh_from_db()
        self.assertEqual(self.rdv.statut, 'annule')
        self.assertTrue(Rendezvous.objects.filter(pk=self.rdv.pk).exists())
        mock_annulation.assert_called_once()
        self.assertEqual(response.status_code, 302)


class DashboardAccessTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()

    def test_non_staff_user_cannot_access_dashboard(self):
        user = self.user_model.objects.create_user(username='user', password='password123')
        self.client.force_login(user)

        response = self.client.get(reverse('dashboard:home'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_staff_user_can_access_dashboard(self):
        user = self.user_model.objects.create_user(username='staff', password='password123', is_staff=True)
        self.client.force_login(user)

        response = self.client.get(reverse('dashboard:home'))
        follow_up = self.client.get(reverse('dashboard:home'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(follow_up.status_code, 200)
