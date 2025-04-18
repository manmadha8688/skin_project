# Generated by Django 5.1.7 on 2025-04-06 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_alter_appointment_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='patient_age',
            field=models.PositiveIntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient_gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10),
        ),
        migrations.AddField(
            model_name='appointment',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
