# Generated by Django 4.2.4 on 2023-10-27 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0013_alter_userprofile_nivel_de_dominio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='nivel_de_dominio',
            field=models.TextField(max_length=50),
        ),
    ]
