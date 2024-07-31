# Generated by Django 5.0.7 on 2024-07-31 14:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AlertType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("channel", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Alert",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("added_date", models.DateTimeField(auto_now_add=True, verbose_name="date created")),
                ("message", models.CharField(max_length=255)),
                (
                    "related_event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="alerts_from_alerts_unique",
                        to="events.event",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SubscribedEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField()),
                ("event_label", models.ManyToManyField(to="events.label")),
                ("event_type", models.ManyToManyField(to="events.eventtype")),
            ],
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("added_date", models.DateTimeField(auto_now_add=True, verbose_name="date created")),
                ("priority", models.IntegerField()),
                ("alert_type", models.ManyToManyField(to="alerts.alerttype")),
                ("suscribed_events", models.ManyToManyField(to="alerts.subscribedevent")),
            ],
        ),
    ]