# Generated by Django 2.2.1 on 2019-05-25 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20190525_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]