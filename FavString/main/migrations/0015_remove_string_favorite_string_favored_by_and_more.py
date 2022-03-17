# Generated by Django 4.0.3 on 2022-03-17 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_string_favorite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='string',
            name='favorite',
        ),
        migrations.AddField(
            model_name='string',
            name='favored_by',
            field=models.ManyToManyField(related_name='favored_by', to='main.user'),
        ),
        migrations.DeleteModel(
            name='FavoriteString',
        ),
    ]
