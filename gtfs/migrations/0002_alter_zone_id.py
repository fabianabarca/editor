# Generated by Django 4.2.5 on 2024-02-22 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtfs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zone',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]