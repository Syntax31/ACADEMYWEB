# Generated by Django 4.2.4 on 2023-12-15 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Group', '0005_joinrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='joinrequest',
            name='message',
        ),
    ]
