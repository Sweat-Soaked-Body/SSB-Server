# Generated by Django 5.1.3 on 2024-12-19 09:58

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('friend', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='friend',
            unique_together={('from_user', 'to_user')},
        ),
    ]