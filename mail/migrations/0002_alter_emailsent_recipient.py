# Generated by Django 4.1.2 on 2022-10-10 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailsent',
            name='recipient',
            field=models.EmailField(max_length=254),
        ),
    ]