# Generated by Django 3.0.7 on 2020-07-07 13:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_models", "0007_auto_20200702_1026"),
    ]

    operations = [
        migrations.AddField(
            model_name="house",
            name="municipality",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="addresses",
                to="data_models.Municipality",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="bbr",
            name="accsses_address",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="buldings",
                to="data_models.House",
            ),
        ),
    ]
