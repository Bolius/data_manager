# Contains the mappings for categorical fields
RECIDENTIAL_TYPE_CHOICES = [
    ("one_fam", "Enfamiliehuse"),
    ("farm", "Stuehuse til landbrug"),
    ("row", "Række/kæde-huse"),
    ("multi", "Dobbelt-/flerfamiliehuse"),
    ("story", "Etageboliger"),
    ("oth", "Anden, herunder kollegier"),
]

HEAT_TYPE_CHOICES = [
    ("1", "Fjernvarme/blokvarme"),
    ("2", "Centralvarme fra eget anlæg, et-kammer fyr"),
    ("3", "Ovne"),
    ("5", "Varmepumpe"),
    ("6", "	Centralvarme med to fyringsenheder"),
    ("7", "Elovne, elpaneler"),
    ("8", "Gasradiator"),
    ("9", "	Ingen varmeinstallation"),
    ("99", "Blandet"),
]

ENERGY_TYPE_CHOICES = [
    ("1", "Gas fra værk"),
    ("2", "230 V el fra værk"),
    ("3", "400 V el fra værk"),
    ("4", "Både 230 V el og gas fra værk"),
    ("5", "Både 400 V el og gas fra værk"),
    ("6", "Hverken el eller gas fra værk"),
]

ROOF_MATERIAL_CHOICES = [
    ("rock", "Cementsten"),
    ("asphalt", "Tagpap"),
    ("builtup", ""),
    ("rockasbt", ""),
    ("brick", ""),
    ("fiber", ""),
    ("green", ""),
    ("metal", ""),
    ("thatched", ""),
    ("pvc", ""),
    ("glas", ""),
    ("oth", ""),
]

WALL_MATERIAL_CHOICES = [
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

energy_labels = (
    ("0", "Ukendt"),
    ("1", "A"),
    ("2", "B"),
    ("3", "C"),
    ("4", "D"),
    ("5", "E"),
    ("6", "F"),
    ("7", "G"),
)

sup_heat_types = (
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
)

heat_instal = (
    ("0", "Ikke oplyst"),
    ("1", "Radiatorsystemer el. varmluftanlæg"),
    ("2", "Centralvarme fra eget anlæg, et-kammer fyr"),
    ("3", "Kakkelovne, kamin, brændeovne og lign."),
    ("5", "Varmepumpe"),
    ("6", "Centralvarme med to fyringsenheder"),
    ("7", "Elovne, elpaneler"),
    ("8", "Gasradiator"),
    ("9", "Ingen varmeinstallation"),
)

water_types = (
    ("0", "Ikke oplyst"),
    ("1", "Alment vandforsyningsanlæg (tidligere offentligt)"),
    ("2", "Privat, alment vandforsyningsanlæg"),
    ("3", "Enkeltindvindingsanlæg (egen boring til 1 eller 2 ejendomme)"),
    ("4", "Brønd"),
    ("6", "Ikke alment vandforsyningsanlæg (forsyner < 10 ejendomme)"),
    ("9", "Ingen vandforsyning"),
)

wall_types = (
    ("1", "Mursten"),
    ("2", "Letbeton"),
    ("3", "Plader af fibercement"),
    ("4", "Bindingsværk"),
    ("5", "Træbeklædning"),
    ("6", "Betonelementer"),
    ("8", "Metalplader"),
    ("10", "Fibercement"),
)

house_types = (
    ("farm", "Stuehuse til landbrug"),
    ("multi", "Dobbelt-/flerfamiliehuse"),
    ("story", "Etageboliger"),
    ("one_fam", "Enfamiliehuse"),
    ("oth", "Anden, herunder kollegier"),
)

categories = {
    "avg_size": "gennemsnits ejendomsstørrelse",
    "avg_nr_rooms": "gennemsnitlig antal værelser",
    "avg_build_year": "gennemsnitlig byggeår",
    "subscript_email": "tilmeldt - email",
    "subscript_garden": "tilmeldt - have",
    "subscript_save_energy": "tilmeldt - spar energi",
    "subscript_climate": "tilmeldt - indeklima",
    "subscript_competition": "tilmeldt - konkurrencer",
    "subscript_cleaning": "tilmeldt - rengøring",
}

WATER_SUPPLY_CHOICES = [
    ("1", "Alment vandforsyningsanlæg (tidligere offentligt)"),
    ("2", "Privat, alment vandforsyningsanlæg"),
    ("3", "	Enkeltindvindingsanlæg (egen boring til 1 eller 2 ejendomme)"),
    ("4", "Brønd"),
    ("6", "Ikke alment vandforsyningsanlæg (forsyner < 10 ejendomme)"),
    ("9", "	Ingen vandforsyning"),
]
