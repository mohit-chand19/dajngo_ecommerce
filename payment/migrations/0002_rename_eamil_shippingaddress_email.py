# Generated by Django 5.1.6 on 2025-03-18 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="shippingaddress",
            old_name="eamil",
            new_name="email",
        ),
    ]
