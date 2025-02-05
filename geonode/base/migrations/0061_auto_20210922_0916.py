# Generated by Django 2.2.20 on 2021-09-22 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0060_auto_20210512_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourcebase',
            name='maintenance_frequency',
            field=models.CharField(blank=True, choices=[('sub_daily', 'Sub-daily'), ('daily', 'Daily'), ('monthly', 'Monthly (12x per year)'), ('quarterly', 'Quarterly (4x per year)'), ('twice_per_year', '2x per year'), ('annually', '1x per year'), ('every_2_to_5_years', '1x every 2 to 5 years'), ('every_6_to_10_years', '1x every 6 to 10 years'), ('every_10_years_or_more', '1x every >10 years'), ('opportunistically', 'opportunistically/highly irregular intervals')], help_text='frequency with which modifications and deletions are made to the data after it is first produced', max_length=255, null=True, verbose_name='maintenance frequency'),
        ),
    ]
