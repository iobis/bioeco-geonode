# Generated by Django 2.2.20 on 2021-09-23 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '0036_auto_20210923_0838'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='url',
            field=models.URLField(blank=True, max_length=2000, null=True),
        ),
    ]