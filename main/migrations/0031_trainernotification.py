# Generated by Django 5.0.1 on 2024-03-22 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_alter_trainersalary_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainerNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notif_msg', models.TextField()),
            ],
        ),
    ]