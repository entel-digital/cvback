# Generated by Django 4.2.5 on 2023-09-19 22:50

from django.db import migrations, models
import django_jsonform.models.fields
import events.models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0002_alter_areaofinterest_geometry"),
    ]

    operations = [
        migrations.AlterField(
            model_name="areaofinterest",
            name="geometry",
            field=django_jsonform.models.fields.ArrayField(
                base_field=django_jsonform.models.fields.ArrayField(
                    base_field=models.FloatField(validators=[events.models.validate_relative]), size=2
                ),
                size=None,
            ),
        ),
    ]
