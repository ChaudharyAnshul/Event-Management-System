# Generated by Django 3.1.7 on 2021-04-04 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20210403_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_rejected',
            field=models.BooleanField(default=False),
        ),
    ]