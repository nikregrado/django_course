# Generated by Django 2.2.1 on 2019-06-09 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_auto_20190609_1719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='key',
        ),
    ]
