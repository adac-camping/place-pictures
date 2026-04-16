from django.test import Client, TestCase
from django.urls import reverse

from image.models import Image


class ImageListViewTests(TestCase):
    def test_groups_images_by_prn_and_filters_by_name(self):
        Image.objects.create(prn="prn:campsite:one", name="alpha.jpg", alt_text="Alpha")
        Image.objects.create(prn="prn:campsite:one", name="beta.jpg")
        Image.objects.create(prn="prn:campsite:two", name="forest.jpg")

        client = Client()
        response = client.get(reverse("image-list"), {"q": "forest"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["query"], "forest")
        self.assertEqual(len(response.context["groups"]), 1)
        self.assertEqual(response.context["groups"][0]["prn"], "prn:campsite:two")
        self.assertEqual(response.context["groups"][0]["image_count"], 1)
