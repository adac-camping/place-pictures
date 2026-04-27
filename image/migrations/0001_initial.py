from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("prn", models.CharField(db_index=True, max_length=100)),
                ("name", models.CharField(max_length=255)),
                ("is_main", models.BooleanField(default=False)),
                ("position", models.IntegerField(default=99)),
                ("alt_text", models.TextField(blank=True)),
                ("crop", models.JSONField(blank=True, null=True)),
                ("tags", models.JSONField(blank=True, default=list)),
                ("partner_id", models.CharField(blank=True, max_length=100, null=True)),
                ("partner_campsite_id", models.CharField(blank=True, max_length=100, null=True)),
                ("source_url", models.URLField(blank=True)),
                ("storage_key", models.CharField(blank=True, max_length=512)),
                ("status", models.CharField(db_index=True, default="active", max_length=32)),
                ("removed_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "image",
                "ordering": ["prn", "-is_main", "position", "name"],
            },
        ),
        migrations.AddConstraint(
            model_name="image",
            constraint=models.UniqueConstraint(fields=("prn", "name"), name="image_prn_name_unique"),
        ),
    ]
