# Generated by Django 4.2.1 on 2023-05-12 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_payment_orderplaced_cart"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="selling_price",
            field=models.FloatField(),
        ),
    ]