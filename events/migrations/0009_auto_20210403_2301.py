# Generated by Django 3.1.7 on 2021-04-03 23:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20210403_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rolerequests',
            name='belongsTo',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.council'),
        ),
    ]