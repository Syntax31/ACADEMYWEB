# Generated by Django 4.2.4 on 2023-10-26 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_userprofile_delete_customuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preferencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='preferencias',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='preferencias',
            field=models.ManyToManyField(to='User.preferencia'),
        ),
    ]
