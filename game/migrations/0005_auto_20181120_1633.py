# Generated by Django 2.1.3 on 2018-11-20 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_delete_userattempt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verb',
            name='verb_type',
            field=models.CharField(choices=[('ichidan', 'Ichidan'), ('godan', 'Godan'), ('suru', '~Suru'), ('kuru', '~Kuru')], max_length=10),
        ),
    ]
