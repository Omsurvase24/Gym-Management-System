# Generated by Django 5.0.1 on 2024-02-01 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_subplan_subplanfeature'),
    ]

    operations = [
        migrations.AddField(
            model_name='subplan',
            name='highlight_status',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
