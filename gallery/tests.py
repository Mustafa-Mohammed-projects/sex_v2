from django.test import TestCase
from django.urls import reverse
from .models import Category, MediaItem


class GalleryTests(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="طبيعة")
        self.video = MediaItem.objects.create(
            title="فيديو تجريبي", kind="video",
            video_url="https://youtu.be/dQw4w9WgXcQ", category=self.cat)
        self.hidden = MediaItem.objects.create(
            title="مخفي", kind="video", video_url="https://youtu.be/dQw4w9WgXcQ",
            is_published=False)

    def test_home_lists_only_published(self):
        r = self.client.get(reverse("gallery:home"))
        self.assertContains(r, "فيديو تجريبي")
        self.assertNotContains(r, "مخفي")

    def test_filter_and_search(self):
        r = self.client.get(reverse("gallery:home"), {"kind": "photo"})
        self.assertNotContains(r, "فيديو تجريبي")
        r = self.client.get(reverse("gallery:home"), {"q": "تجريبي"})
        self.assertContains(r, "فيديو تجريبي")

    def test_detail_counts_views_and_embeds(self):
        r = self.client.get(self.video.get_absolute_url())
        self.assertContains(r, "youtube.com/embed/dQw4w9WgXcQ")
        self.video.refresh_from_db()
        self.assertEqual(self.video.views, 1)

    def test_hidden_item_404(self):
        self.assertEqual(self.client.get(self.hidden.get_absolute_url()).status_code, 404)
