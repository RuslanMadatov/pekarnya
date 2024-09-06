# Generated by Django 4.2 on 2023-12-12 16:42

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255, verbose_name='Тема письма')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('email', models.EmailField(max_length=255)),
                ('content', models.TextField(verbose_name='Содержимое письма')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')),
            ],
            options={
                'verbose_name': 'Обратная связь',
                'verbose_name_plural': 'Обратная связь',
                'db_table': 'app_feedback',
                'ordering': ['-time_create'],
            },
        ),
    ]
