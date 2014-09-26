import datetime

from django.utils import timezone
from django.test import TestCase

from models import AnnotatedImage


class AnnotatedImageMethodTests(TestCase):
    def test_was_published_recently_with_future_annotatedimage(self):
        """
        was_computed_recently() should return False for questions whose
        comp_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_image = AnnotatedImage(comp_date=time)
        self.assertEqual(future_image.was_computed_recently(), False)