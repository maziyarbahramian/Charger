# Generated by Django 5.0.1 on 2024-02-03 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_rename_phone_number_phonenumber_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chargerequest',
            old_name='requested_credit_amount',
            new_name='amount',
        ),
    ]
