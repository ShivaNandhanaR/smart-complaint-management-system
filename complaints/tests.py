from django.test import TestCase
from django.contrib.auth.models import User
from .models import Complaint


class ComplaintTestCase(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_complaint_creation(self):

        complaint = Complaint.objects.create(
            user=self.user,
            category='Plumbing',
            location='Block A',
            description='Water leakage',
            priority='High'
        )

        self.assertEqual(
            complaint.category,
            'Plumbing'
        )

        self.assertEqual(
            complaint.status,
            'Submitted'
        )