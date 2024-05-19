# Generated by Django 5.0.6 on 2024-05-12 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SalesData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('revenue', models.DecimalField(decimal_places=2, max_digits=10)),
                ('expenses', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
