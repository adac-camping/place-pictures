from django.core.management.base import BaseCommand

from image.models import Image
from image.services import generate_placeholder_tags


class Command(BaseCommand):
    help = "Generate tags for images that do not have tags yet."

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=100,
            help="Maximum number of images to process in one run.",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Retag images even if tags already exist.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show which images would be tagged without saving changes.",
        )

    def handle(self, *args, **options):
        queryset = Image.objects.order_by("id")
        if not options["force"]:
            queryset = queryset.filter(tags=[])

        images = list(queryset[: options["limit"]])
        if not images:
            self.stdout.write(self.style.SUCCESS("No images to tag."))
            return

        tagged_count = 0
        for image in images:
            image.tags = generate_placeholder_tags(image)
            if not options["dry_run"]:
                image.save(update_fields=["tags", "updated_at"])
            tagged_count += 1
            self.stdout.write(f"Tagged {image.prn} / {image.name}")

        suffix = " (dry-run)" if options["dry_run"] else ""
        self.stdout.write(self.style.SUCCESS(f"Processed {tagged_count} image(s){suffix}."))
