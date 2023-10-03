# Generated by Django 4.2.5 on 2023-09-19 20:31

from django.db import migrations, models
import django_jsonform.models.fields


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="areaofinterest",
            name="geometry",
            field=django_jsonform.models.fields.ArrayField(
                base_field=django_jsonform.models.fields.ArrayField(base_field=models.FloatField(), size=2), size=None
            ),
        ),
    ]