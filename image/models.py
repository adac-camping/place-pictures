from django.db import models


class Image(models.Model):
    prn = models.CharField(max_length=100, db_index=True)
    name = models.CharField(max_length=255)
    is_main = models.BooleanField(default=False)
    position = models.IntegerField(default=99)
    alt_text = models.TextField(blank=True)
    crop = models.JSONField(null=True, blank=True)
    tags = models.JSONField(default=list, blank=True)
    partner_id = models.CharField(max_length=100, null=True, blank=True)
    partner_campsite_id = models.CharField(max_length=100, null=True, blank=True)
    source_url = models.URLField(blank=True)
    storage_key = models.CharField(max_length=512, blank=True)
    status = models.CharField(max_length=32, default="active", db_index=True)
    removed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "image"
        ordering = ["prn", "-is_main", "position", "name"]
        constraints = [
            models.UniqueConstraint(fields=["prn", "name"], name="image_prn_name_unique")
        ]

    def __str__(self):
        return f"{self.prn} / {self.name}"
