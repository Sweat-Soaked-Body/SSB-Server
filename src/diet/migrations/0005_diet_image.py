# Generated by Django 5.1.4 on 2024-12-30 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("diet", "0004_diet_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="diet",
            name="image",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
