# Generated by Django 4.2.7 on 2024-02-15 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_trainerachivement'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainer',
            name='salary',
            field=models.IntegerField(null=True),
        ),
    ]