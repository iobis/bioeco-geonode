# Generated by Django 2.2.20 on 2021-09-21 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goos', '0001_initial'),
        ('layers', '0034_auto_20210329_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='eovs',
            field=models.ManyToManyField(blank=True, to='goos.Eov'),
        ),
    ]