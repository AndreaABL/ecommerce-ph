# Generated by Django 4.1.7 on 2023-10-31 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_delete_irrigat_rename_name_information_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='information',
            name='name',
            field=models.CharField(default=True, max_length=100),
        ),
    ]