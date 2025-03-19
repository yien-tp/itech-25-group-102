from django.test import TestCase
from django.contrib.auth.models import User
from trails_web.models import Trail, Category, UserProfile

class TrailModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category", slug="test-category")
        self.trail = Trail.objects.create(
            title="Test Trail",
            length=5.0,
            estimate_time=2.5,
            level="Easy",
            elevation_gain=100,
            latitude=55.12345,
            longitude=-4.54321,
            category=self.category
        )

    def test_trail_str(self):
        """Check the string representation of the Trail model."""
        self.assertEqual(str(self.trail), "Test Trail")

    def test_trail_category(self):
        """Verify the trail's category is set correctly."""
        self.assertEqual(self.trail.category, self.category)

    def test_trail_rounding(self):
        """Ensure the trail's estimate_time is rounded to 2 decimals on save."""
        self.trail.estimate_time = 2.123456
        self.trail.save()
        self.assertEqual(self.trail.estimate_time, 2.12)