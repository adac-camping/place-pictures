from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from image.models import Image


class TagImagesCommandTests(TestCase):
    def test_tags_only_untagged_images_by_default(self):
        untagged = Image.objects.create(prn="prn:campsite:one", name="lake-view.jpg")
        tagged = Image.objects.create(
            prn="prn:campsite:two",
            name="forest.jpg",
            tags=[{"key": "forest", "confidence": 0.91}],
        )

        output = StringIO()
        call_command("tag_images", stdout=output)

        untagged.refresh_from_db()
        tagged.refresh_from_db()

        self.assertTrue(untagged.tags)
        self.assertEqual(tagged.tags, [{"key": "forest", "confidence": 0.91}])
        self.assertIn("Processed 1 image(s).", output.getvalue())

    def test_dry_run_does_not_persist_tags(self):
        image = Image.objects.create(prn="prn:campsite:one", name="tent-lake.jpg")

        call_command("tag_images", "--dry-run")
        image.refresh_from_db()

        self.assertEqual(image.tags, [])
