# Generated by Django 4.0.3 on 2022-03-17 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_favoritestring_strings_favoritestring_strings_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favoritestring',
            old_name='strings',
            new_name='string',
        ),
    ]
