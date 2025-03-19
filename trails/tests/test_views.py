from django.test import TestCase
from django.urls import reverse
from trails_web.models import Trail, Category

class TrailDetailViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Category", slug="category")
        self.trail = Trail.objects.create(
            title="Sample Trail",
            length=4.0,
            estimate_time=1.5,
            level="Easy",
            elevation_gain=200,
            latitude=55.0,
            longitude=-4.0,
            category=self.category
        )
        self.detail_url = reverse('trails_web:trail_detail', args=[self.trail.id])

    def test_trail_detail_view_status_code(self):
        """Ensure the trail detail page returns 200."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)

    def test_trail_detail_view_template_used(self):
        """Check that the correct template is used."""
        response = self.client.get(self.detail_url)
        self.assertTemplateUsed(response, 'trails_web/trail_detail.html')

    def test_trail_detail_view_content(self):
        """Verify the trail title appears in the response."""
        response = self.client.get(self.detail_url)
        self.assertContains(response, "Sample Trail")