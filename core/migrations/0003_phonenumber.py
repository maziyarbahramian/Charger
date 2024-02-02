# Generated by Django 5.0.1 on 2024-02-02 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_creditrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=20)),
                ('charge', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True)),
            ],
        ),
    ]