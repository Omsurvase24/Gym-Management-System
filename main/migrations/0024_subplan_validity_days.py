# Generated by Django 4.2.7 on 2024-02-14 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_alter_assignsubscriber_trainer'),
    ]

    operations = [
        migrations.AddField(
            model_name='subplan',
            name='validity_days',
            field=models.IntegerField(null=True),
        ),
    ]