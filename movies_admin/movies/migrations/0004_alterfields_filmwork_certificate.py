# Generated by Django 3.2 on 2023-04-07 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_addfields_person_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmwork',
            name='certificate',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='certificate'),
        ),
    ]