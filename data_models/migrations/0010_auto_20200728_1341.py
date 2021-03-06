# Generated by Django 3.0.7 on 2020-07-28 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_models", "0009_auto_20200728_1336"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bbr",
            name="heat_install",
            field=models.CharField(
                choices=[
                    ("0", "Ikke oplyst"),
                    ("1", "Fjernvarme/blokvarme"),
                    ("2", "Centralvarme fra eget anlæg, et-kammer fyr"),
                    ("3", "Ovne"),
                    ("5", "Varmepumpe"),
                    ("6", "Centralvarme med to fyringsenheder"),
                    ("7", "Elovne, elpaneler"),
                    ("8", "Gasradiator"),
                    ("9", "Ingen varmeinstallation"),
                    ("99", "Blandet"),
                ],
                max_length=2,
                null=True,
                verbose_name="Primær varmeinstallation",
            ),
        ),
    ]
