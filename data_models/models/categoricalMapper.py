# Contains the mappings for categorical fields
HEAT_INSTALL_CHOICES = [
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
]

HEAT_TYPE_CHOICES = [
    ("0", "Ikke oplyst"),
    ("1", "Elektricitet"),
    ("2", "Gasværksgas"),
    ("3", "Flydende brændsel"),
    ("4", "Fast brændsel"),
    ("6", "Halm"),
    ("7", "Naturgas"),
    ("9", "Andet"),
]

HEAT_SUPPLY_INSTALL_CHOICES = [
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
]

WATER_SUPPLY_CHOICES = [
    ("0", "Ikke oplyst"),
    ("1", "Alment vandforsyningsanlæg (tidligere offentligt)"),
    ("2", "Privat, alment vandforsyningsanlæg"),
    ("3", "	Enkeltindvindingsanlæg (egen boring til 1 eller 2 ejendomme)"),
    ("4", "Brønd"),
    ("6", "Ikke alment vandforsyningsanlæg (forsyner < 10 ejendomme)"),
    ("9", "	Ingen vandforsyning"),
]

WALL_MATERIAL_CHOICES = [
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
]

ENERGY_SUPPLY_CHOICES = [
    ("0", "Ikke oplyst"),
    ("1", "Gas fra værk"),
    ("2", "230 V el fra værk"),
    ("3", "400 V el fra værk"),
    ("4", "Både 230 V el og gas fra værk"),
    ("5", "Både 400 V el og gas fra værk"),
    ("6", "Hverken el eller gas fra værk"),
]

ROOFING_MATERIAL_CHOICES = [
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
]

PROPERTY_TYPE_CHOICES = [
    ("0", "Ikke oplyst"),
    ("1", "Egentlig beboelseslejlighed"),
    ("2", "Blandet erhverv og bolig med eget køkken."),
    ("3", "Enkeltværelse"),
    ("4", "Fællesbolig eller fælleshusholdning"),
    ("5", "Sommer-/fritidsbolig."),
    ("E", "Andet (bl.a. institutioner og erhverv)"),
]

KITCHEN_FACILITY = [
    ("0", "Ikke oplyst"),
    ("E", "Eget køkken"),
    ("F", "Adgang til fælles køkken"),
    ("G", "Fast kogeinstallation i værelse eller på gang"),
    ("H", "Ingen fast kogeinstallation"),
]

TOILET_FACILITY = [
    ("0", "Ikke oplyst"),
    ("T", "Vandskyllende toilet i bolig- eller erhvervsenheden"),
    ("A", "Vandskyllende toilet udenfor enheden"),
    (
        "B",
        "Anden type toilet udenfor enheden eller intet toilet i B forbindelse med enheden",
    ),
]

BATHING_FACILITY = [
    ("0", "Ikke oplyst"),
    ("V", "Badeværelser i enheden"),
    ("C", "Adgang til badeværelse"),
    ("D", "Hverken badeværelse eller adgang til badeværelse"),
]

#
#
#
#
#

RECIDENTIAL_TYPE_CHOICES = [
    ("one_fam", "Enfamiliehuse"),
    ("farm", "Stuehuse til landbrug"),
    ("row", "Række/kæde-huse"),
    ("multi", "Dobbelt-/flerfamiliehuse"),
    ("story", "Etageboliger"),
    ("oth", "Anden, herunder kollegier"),
]
