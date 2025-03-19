from django.test import TestCase
from trails_web.forms import TrailForm

class TrailFormTest(TestCase):
    def test_valid_data(self):
        """A valid form should be recognized as valid."""
        form_data = {
            'title': 'Form Trail',
            'length': 3.5,
            'estimate_time': 1.5,
            'level': 'Easy',
            'elevation_gain': 150,
            'latitude': 55.1234,
            'longitude': -4.5678,
        }
        form = TrailForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_title(self):
        """Missing title should make the form invalid."""
        form_data = {
            'length': 3.5,
            'estimate_time': 1.5,
            'level': 'Easy',
            'elevation_gain': 150,
            'latitude': 55.1234,
            'longitude': -4.5678,
        }
        form = TrailForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)