# Generated by Django 2.2.20 on 2021-09-23 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '0035_layer_eovs'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='readiness_coordination',
            field=models.CharField(blank=True, choices=[('1', 'Level 1 - Idea'), ('2', 'Level 2 - Documentation'), ('3', 'Level 3 - Proof of concept'), ('4', 'Level 4 - Trial'), ('5', 'Level 5 - Verification'), ('6', 'Level 6 - Operational'), ('7', 'Level 7 - Fitness for purpose'), ('8', 'Level 8 - Mission qualified'), ('9', 'Level 9 - Sustained')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='layer',
            name='readiness_data',
            field=models.CharField(blank=True, choices=[('1', 'Level 1 - Idea'), ('2', 'Level 2 - Documentation'), ('3', 'Level 3 - Proof of concept'), ('4', 'Level 4 - Trial'), ('5', 'Level 5 - Verification'), ('6', 'Level 6 - Operational'), ('7', 'Level 7 - Fitness for purpose'), ('8', 'Level 8 - Mission qualified'), ('9', 'Level 9 - Sustained')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='layer',
            name='readiness_requirements',
            field=models.CharField(blank=True, choices=[('1', 'Level 1 - Idea'), ('2', 'Level 2 - Documentation'), ('3', 'Level 3 - Proof of concept'), ('4', 'Level 4 - Trial'), ('5', 'Level 5 - Verification'), ('6', 'Level 6 - Operational'), ('7', 'Level 7 - Fitness for purpose'), ('8', 'Level 8 - Mission qualified'), ('9', 'Level 9 - Sustained')], max_length=100, null=True),
        ),
    ]