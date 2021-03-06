# Generated by Django 3.0.7 on 2020-07-28 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_models", "0008_auto_20200707_1509"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bbr",
            name="heat_type",
            field=models.CharField(
                choices=[
                    ("0", "Ikke oplyst"),
                    ("1", "Elektricitet"),
                    ("2", "Gasværksgas"),
                    ("3", "Flydende brændsel"),
                    ("4", "Fast brændsel"),
                    ("6", "Halm"),
                    ("7", "Naturgas"),
                    ("9", "Andet"),
                ],
                max_length=2,
                null=True,
                verbose_name="Primært Opvarmningsmiddel",
            ),
        ),
    ]
