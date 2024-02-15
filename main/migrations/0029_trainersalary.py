# Generated by Django 4.2.7 on 2024-02-15 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_trainer_salary'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainerSalary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amt', models.IntegerField()),
                ('amt_date', models.DateField()),
                ('remarks', models.TextField()),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.trainer')),
            ],
        ),
    ]
