# Generated by Django 3.0.8 on 2020-09-11 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20200909_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voteentry',
            name='voted_option',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='polls.PollOption'),
        ),
    ]