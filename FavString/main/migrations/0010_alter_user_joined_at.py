# Generated by Django 4.0.3 on 2022-03-17 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_string_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='joined_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
