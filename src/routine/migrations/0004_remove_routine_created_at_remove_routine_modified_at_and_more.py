# Generated by Django 5.1.3 on 2024-12-19 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routine', '0003_set_time_alter_set_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='routine',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='routine',
            name='modified_at',
        ),
        migrations.AddField(
            model_name='routine',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
