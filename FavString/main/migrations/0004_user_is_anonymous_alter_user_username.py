# Generated by Django 4.0.3 on 2022-03-17 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_user_is_authenticated'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_anonymous',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]