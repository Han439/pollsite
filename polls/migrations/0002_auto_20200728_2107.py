# Generated by Django 3.0.8 on 2020-07-28 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollquestion',
            name='tag',
            field=models.ManyToManyField(blank=True, to='polls.Tag'),
        ),
    ]
