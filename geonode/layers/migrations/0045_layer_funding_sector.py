# Generated by Django 2.2.20 on 2022-04-29 08:48

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '0044_layer_funding'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='funding_sector',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('academia', 'Academia'), ('civil_society', 'Civil society'), ('industry', 'Industry'), ('governmental', 'Governmental'), ('other', 'Other')], max_length=30), blank=True, null=True, size=None),
        ),
    ]
