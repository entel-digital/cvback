# Generated by Django 4.2.5 on 2024-02-13 02:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("devices", "0005_alter_camera_primary_stream"),
    ]

    operations = [
        migrations.CreateModel(
            name="Area",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("added_date", models.DateTimeField(auto_now_add=True, verbose_name="date created")),
                ("added_modified", models.DateTimeField(auto_now=True, verbose_name="date modified")),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name="camera",
            name="area",
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="devices.area"),
        ),
    ]