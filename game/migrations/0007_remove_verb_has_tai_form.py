# Generated by Django 2.1.3 on 2018-11-27 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_verb_has_tai_form'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='verb',
            name='has_tai_form',
        ),
    ]