# Generated by Django 4.1.7 on 2023-10-10 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_information'),
    ]

    operations = [
        migrations.AddField(
            model_name='information',
            name='name',
            field=models.CharField(default=True, max_length=100),
        ),
    ]