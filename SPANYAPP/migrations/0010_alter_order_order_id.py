# Generated by Django 5.1 on 2025-01-16 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("SPANYAPP", "0009_orderitems"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="order_id",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
