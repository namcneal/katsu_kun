# Generated by Django 2.1.3 on 2018-11-20 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_userattempt'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserAttempt',
        ),
    ]
