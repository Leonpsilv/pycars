# Generated by Django 4.2.3 on 2023-07-12 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avatars', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='avatarmodel',
            name='filename',
            field=models.CharField(default=''),
        ),
    ]
