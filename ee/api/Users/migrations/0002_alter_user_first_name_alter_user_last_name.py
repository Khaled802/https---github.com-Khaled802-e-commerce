# Generated by Django 4.1.5 on 2023-01-25 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_Users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
