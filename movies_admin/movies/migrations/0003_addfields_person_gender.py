# Generated by Django 3.2 on 2023-04-07 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_addfields_filmwork_certiicate_file_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='gender',
            field=models.TextField(choices=[('male', 'male'), ('female', 'female')], null=True, verbose_name='gender'),
        ),
    ]
