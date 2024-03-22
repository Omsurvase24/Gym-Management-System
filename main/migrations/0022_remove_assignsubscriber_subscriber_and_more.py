# Generated by Django 4.2.7 on 2024-02-13 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0021_assignsubscriber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignsubscriber',
            name='subscriber',
        ),
        migrations.AddField(
            model_name='assignsubscriber',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]