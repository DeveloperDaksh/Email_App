# Generated by Django 2.1.5 on 2021-08-18 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0002_auto_20210818_1442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailusers',
            name='email_prefix',
        ),
        migrations.AddField(
            model_name='emailusers',
            name='email_default',
            field=models.EmailField(default=90, max_length=255),
            preserve_default=False,
        ),
    ]
