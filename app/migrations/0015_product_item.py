# Generated by Django 4.1.7 on 2023-06-16 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_category_subcategory_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='item',
            field=models.BooleanField(default=False, help_text='0=default, 1=item'),
        ),
    ]
