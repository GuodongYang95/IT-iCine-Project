# Generated by Django 2.1.5 on 2020-03-13 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_motto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='motto',
            field=models.TextField(default='Moive lover', max_length=64),
        ),
    ]
