# Generated by Django 2.2.1 on 2019-05-25 19:55

from django.db import migrations, models
import polls.models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_game_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='image',
            field=models.ImageField(upload_to=polls.models.image_folder),
        ),
    ]