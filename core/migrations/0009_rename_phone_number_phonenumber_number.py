# Generated by Django 5.0.1 on 2024-02-03 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_transaction_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='phonenumber',
            old_name='phone_number',
            new_name='number',
        ),
    ]
