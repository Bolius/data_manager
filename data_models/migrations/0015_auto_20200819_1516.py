# Generated by Django 3.1 on 2020-08-19 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_models", "0014_auto_20200729_1621"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bbr",
            name="bathing_facility",
            field=models.CharField(
                choices=[
                    ("0", "Ikke oplyst"),
                    ("V", "Badeværelser i enheden"),
                    ("C", "Adgang til badeværelse"),
                    ("D", "Hverken badeværelse eller adgang til badeværelse"),
                ],
                default="0",
                max_length=2,
                verbose_name="badeforhold",
            ),
        ),
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
                default="0",
                max_length=2,
                verbose_name="Primær varmeinstallation",
            ),
        ),
        migrations.AlterField(
            model_name="bbr",
            name="heat_supply",
            field=models.CharField(
                choices=[
                    ("0", "Ikke oplyst"),
                    ("1", "Varmepumpeanlæg"),
                    ("2", "Brændeovn o. lign."),
                    ("3", "Ovne til flydende brændsel"),
                    ("4", "Solpaneler"),
                    ("5", "Pejs"),
                    ("6", "Gasradiator"),
                    ("7", "Elovne, elpaneler"),
                    ("10", "Biogasanlæg"),
                    ("80", "Andet"),
                    ("90", "Ingen"),
                ],
                default="0",
                max_length=2,
                verbose_name="Supplerende Varmekilde",
            ),
        ),
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
                default="0",
                max_length=2,
                verbose_name="Primært Opvarmningsmiddel",
            ),
        ),
        migrations.AlterField(
            model_name="bbr",
            name="kitchen_facility",
            field=models.CharField(
                choices=[
                    ("0", "Ikke oplyst"),
                    ("E", "Eget køkken"),
                    ("F", "Adgang til fælles køkken"),
                    ("G", "Fast kogeinstallation i værelse eller på gang"),
                    ("H", "Ingen fast kogeinstallation"),
                ],
                default="0",
                max_length=2,
                verbose_name="køkkenforhold",
            ),
        ),
        migrations.AlterField(
            model_name="bbr",
            name="property_type",
            field=models.CharField(
                choices=[
                    ("0", "Ikke oplyst"),
                    ("1", "Egentlig beboelseslejlighed"),
                    ("2", "Blandet erhverv og bolig med eget køkken."),
                    ("3", "Enkeltværelse"),
                    ("4", "Fællesbolig eller fælleshusholdning"),
                    ("5", "Sommer-/fritidsbolig."),
                    ("E", "Andet (bl.a. institutioner og erhverv)"),
                ],
                default="0",
                max_length=2,
                verbose_name="Boligtype",
            ),
        ),
        migrations.AlterField(
            model_name="bbr",
            name="roofing_material",
            field=models.CharField(
                choices=[
                    ("0", "Ikke oplyst"),
                    ("1", "Built-up"),
                    ("2", "Tagpap"),
                    ("3", "Fibercement"),
                    ("4", "Cementsten"),
                    ("5", "Tegl"),
                    ("6", "Metalplader"),
                    ("7", "Stråtag"),
                    ("10", "Fibercement"),
                    ("11", "PVC"),
                    ("12", "Glas"),
                    ("20", "Grønne tage"),
                    ("80", "Ingen"),
                    ("90", "Andet materiale"),
                ],
                default="0",
                max_length=2,
                verbose_name="Tagdækningsmateriale",
            ),
        ),
        migrations.AlterField(
            model_name="bbr",
            name="toilet_facility",
            field=models.CharField(
                choices=[
                    ("0", "Ikke oplyst"),
                    ("T", "Vandskyllende toilet i bolig- eller erhvervsenheden"),
                    ("A", "Vandskyllende toilet udenfor enheden"),
                    (
                        "B",
                        "Anden type toilet udenfor enheden eller intet toilet i B forbindelse med enheden",
                    ),
                ],
                default="0",
                max_length=2,
                verbose_name="Toiletforhold",
            ),
        ),
        migrations.AlterField(
            model_name="bbr",
            name="wall_material",
            field=models.CharField(
                choices=[
                    ("0", "Ikke oplyst"),
                    ("1", "Mursten"),
                    ("2", "Letbeton"),
                    ("3", "Plader af fibercement"),
                    ("4", "Bindingsværk"),
                    ("5", "Træbeklædning"),
                    ("6", "Betonelementer (etagehøje betonelementer)"),
                    ("8", "Metalplader"),
                    ("10", "Fibercement (asbestfri)"),
                    ("11", "PVC"),
                    ("12", "Glas"),
                    ("80", "Ingen"),
                    ("90", "Andet materiale"),
                ],
                default="0",
                max_length=2,
                verbose_name="Ydervægs Materiale",
            ),
        ),
        migrations.AlterField(
            model_name="bbr",
            name="water_supply",
            field=models.CharField(
                choices=[
                    ("0", "Ikke oplyst"),
                    ("1", "Alment vandforsyningsanlæg (tidligere offentligt)"),
                    ("2", "Privat, alment vandforsyningsanlæg"),
                    (
                        "3",
                        "\tEnkeltindvindingsanlæg (egen boring til 1 eller 2 ejendomme)",
                    ),
                    ("4", "Brønd"),
                    ("6", "Ikke alment vandforsyningsanlæg (forsyner < 10 ejendomme)"),
                    ("9", "\tIngen vandforsyning"),
                ],
                default="0",
                max_length=2,
                verbose_name="Vandforsyning",
            ),
        ),
    ]