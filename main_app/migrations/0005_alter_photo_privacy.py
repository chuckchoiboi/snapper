# Generated by Django 3.2 on 2021-05-01 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_photo_privacy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='privacy',
            field=models.BooleanField(default=False),
        ),
    ]