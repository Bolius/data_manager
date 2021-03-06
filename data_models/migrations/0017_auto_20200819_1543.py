# Generated by Django 3.1 on 2020-08-19 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_models", "0016_auto_20200819_1534"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bbr",
            name="residential_type",
            field=models.CharField(
                choices=[
                    ("120", "Enfamiliehuse"),
                    ("110", "Stuehuse til landbrug"),
                    ("130", "Række/kæde-huse"),
                    ("131", "Række- og kædehus (lodret adskillelse mellem enhederne)"),
                    (
                        "140",
                        "Etagebolig-bygning, flerfamilehus eller to- familiehus (vandret adskillelse mellem enhederne)",
                    ),
                    (
                        "132",
                        "Dobbelthus (to boliger med lodret adskillelse mellem enhederne)",
                    ),
                    ("multi", "Dobbelt-/flerfamiliehuse"),
                    ("321", "Bygning til kontor"),
                    ("412", "Museum"),
                    ("322", "Bygning til handel og butik"),
                    ("323", "Bygning til lager"),
                    ("510", "Sommerhus"),
                    ("540", "Kolonihavehus"),
                    ("story", "Etageboliger"),
                    ("oth", "Anden, herunder kollegier"),
                ],
                max_length=7,
                verbose_name="Boligtype",
            ),
        ),
    ]
