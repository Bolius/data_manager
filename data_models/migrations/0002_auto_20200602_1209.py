# Generated by Django 3.0.5 on 2020-06-02 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("data_models", "0001_delete_appaction"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="municipality",
            options={
                "ordering": ["name"],
                "verbose_name": "Kommune",
                "verbose_name_plural": "Kommuner",
            },
        ),
    ]
