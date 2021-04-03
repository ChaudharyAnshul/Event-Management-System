# Generated by Django 3.1.7 on 2021-04-03 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffIdMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100)),
                ('eid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='StudentIdMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100)),
                ('iid', models.IntegerField()),
            ],
        ),
    ]