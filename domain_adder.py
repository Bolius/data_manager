from data_models.models import Domain

own_types_ = {
    "name": "Ejerforhold",
    "type": "categorical",
    "description": "Ejerforhold er udledt af Geomatic baseret på oplysninger i BBR og ESR.",
    "source": "BBR",
    "values": (
        ("own", "Ejerbolig"),
        ("pri_rent", "Privat Leje"),
        ("pub_rent", "Offentligt Leje"),
        ("part", "Andelsbolig"),
        ("unk", "Ukendt"),
    ),
}

heat_types_ = {
    "name": "Opvarmningsform",
    "type": "categorical",
    "description": "Afledt opvarmningsmiddel beregnet af Geomatic baseret på BBR data.",
    "source": "BBR",
    "values": (
        ("remote", "Fjernvarme"),
        ("gas", "Naturgas"),
        ("liquid", "Flydene brændsel"),
        ("elec", "Elektricitet"),
        ("oth", "Andet"),
    ),
}

roof_types_ = {
    "name": "Tag type",
    "type": "catagorical",
    "description": "Simplificeret tagmateriale variabel, som kun indeholder kategorier for de mest almindelige typer af tagmateriale.",
    "source": "BBR",
    "values": (
        ("fiber", "Fibercement"),
        ("rock", "Cementsten"),
        ("clay", "Tegl"),
        ("asphalt", "Tagpap"),
        ("oth", "Andet"),
    ),
}

energy_types_ = {
    "name": "Energiforsying",
    "type": "categorical",
    "description": "Energiforsyning stammer fra den primære bolig-/erhvervsenhed på enhedsadressen. I tilfælde af flere bolig-/erhvervsenheder på samme enhedsadresse, angiver den primære enhed den enhed som mest sandsynligt anvendes til privat beboelse.",
    "source": "BBR",
    "values": (
        ("0", "Ukendt"),
        ("1", "Gas fra værk"),
        ("2", "230 V el fra værk"),
        ("3", "400 V el fra værk"),
        ("4", "Både 230 V el og gas fra værk"),
        ("5", "Både 400 V el og gas fra værk"),
    ),
}

energy_labels_ = {
    "name": "Energimærke",
    "type": "categorical",
    "description": " ",
    "source": "boliga",
    "values": (
        ("0", "Ukendt"),
        ("1", "A"),
        ("2", "B"),
        ("3", "C"),
        ("4", "D"),
        ("5", "E"),
        ("6", "F"),
        ("7", "G"),
    ),
}

sup_heat_types_ = {
    "name": "Supplerende varmeinstallation",
    "type": "categorical",
    "description": " ",
    "source": "BBR",
    "values": (
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
    ),
}

heat_install_ = {
    "name": "Varmeinstallation",
    "type": "categorical",
    "description": " ",
    "source": "BBR",
    "values": (
        ("0", "Ikke oplyst"),
        ("1", "Radiatorsystemer el. varmluftanlæg"),
        ("2", "Centralvarme fra eget anlæg, et-kammer fyr"),
        ("3", "Kakkelovne, kamin, brændeovne og lign."),
        ("5", "Varmepumpe"),
        ("6", "Centralvarme med to fyringsenheder"),
        ("7", "Elovne, elpaneler"),
        ("8", "Gasradiator"),
        ("9", "Ingen varmeinstallation"),
    ),
}

water_types_ = {
    "name": "Vandforsyning",
    "type": "categorical",
    "description": " ",
    "source": "BBR",
    "values": (
        ("0", "Ikke oplyst"),
        ("1", "Alment vandforsyningsanlæg (tidligere offentligt)"),
        ("2", "Privat, alment vandforsyningsanlæg"),
        ("3", "Enkeltindvindingsanlæg (egen boring til 1 eller 2 ejendomme)"),
        ("4", "Brønd"),
        ("6", "Ikke alment vandforsyningsanlæg (forsyner < 10 ejendomme)"),
        ("9", "Ingen vandforsyning"),
    ),
}

wall_types_ = {
    "name": "Ydervægsmateriale",
    "type": "categorical",
    "description": " ",
    "source": "BBR",
    "values": (
        ("1", "Mursten"),
        ("2", "Letbeton"),
        ("3", "Plader af fibercement"),
        ("4", "Bindingsværk"),
        ("5", "Træbeklædning"),
        ("6", "Betonelementer"),
        ("8", "Metalplader"),
        ("10", "Fibercement"),
    ),
}

house_types_ = {
    "name": "Boligtype",
    "type": "categorical",
    "description": "Geomatic's definition af boligtype baseret på BBR data.",
    "source": "BBR",
    "values": (
        ("farm", "Stuehuse til landbrug"),
        ("multi", "Dobbelt-/flerfamiliehuse"),
        ("story", "Etageboliger"),
        ("one_fam", "Enfamiliehuse"),
        ("oth", "Anden, herunder kollegier"),
    ),
}

size_ = {
    "name": "Boligstørrelse",
    "type": "scalar",
    "description": "Areal af samtlige beboelsesrum incl. køkken, bad, wc-rum, herunder boligareal i udnyttet tagetage. I kælderetage medtages arealet af de rum, der må anvendes til beboelse i henhold til byggelovgivningen samt arealet af køkken, baderum og wc-rum. Arealet måles til ydersiden af ydervægge (bruttoetageareal). Arealet inkluderer andel af adgangsarealer. ",
    "source": "BBR",
    "value": "size",
}

bis_area_ = {
    "name": "Erhvervs areal",
    "type": "scalar",
    "description": "Omfatter arealet af samtlige rum, der udelukkende anvendes til erhverv (ikke-boligformål), herunder også udnyttet areal af tagetage og kælderetage. Arealet måles til ydersiden af ydervægge (bruttoetageareal). Arealet er incl. andel af adgangsarealer og erhvervsmæssigt anvendt garageareal. Areal til erhverv stammer fra den primære bolig-/erhvervsenhed på enhedsadressen. ",
    "source": "BBR",
    "value": "bis_area",
}

oth_area_ = {
    "name": "Andet areal",
    "type": "scalar",
    "description": "Areal der hverken er erhverv eller beboelse f.eks. kælderareal eller loftrum, der er tinglyst på ejerlejlighed.",
    "source": "BBR",
    "value": "oth_area",
}

nr_rooms_ = {
    "name": "Antal værelser",
    "type": "scalar",
    "description": " ",
    "source": "BBR",
    "value": "nr_rooms",
}

nr_baths_ = {
    "name": "Antal badeværelse",
    "type": "scalar",
    "description": " ",
    "source": "BBR",
    "value": "nr_baths",
}

nr_toilets_ = {
    "name": "Antal toiletter",
    "type": "scalar",
    "description": " ",
    "source": "BBR",
    "value": "nr_toilets",
}

total_area_ = {
    "name": "Total areal",
    "type": "scalar",
    "description": " ",
    "source": "BBR",
    "value": "total_area",
}

basement_area_ = {
    "name": "Kælder areal",
    "type": "scalar",
    "description": "	Det opsummerede areal for alle kælderetager i bygningen. Kælderetager er etager som har en etagebetegnelse som begynder med K.",
    "source": "BBR",
    "value": "basement_area",
}

basement_area_used_ = {
    "name": "Benyttet kælder areal",
    "type": "scalar",
    "description": "Areal af lovlig beboelse i kælder",
    "source": "BBR",
    "value": "basement_area_used",
}

roof_area_ = {
    "name": "Tagareal",
    "type": "scalar",
    "description": "Det opsummerede areal for alle tagetager i bygningen. Etagetypen fortæller om en etage er en tagetage.",
    "source": "BBR",
    "value": "roof_area",
}

nr_of_floors_ = {
    "name": "Antal etager",
    "type": "scalar",
    "description": " ",
    "source": "BBR",
    "value": "nr_of_floors",
}

out_room_size_ = {
    "name": "Udestue størrelse",
    "type": "scalar",
    "description": "",
    "source": "BBR",
    "value": "out_room_size",
}

garage_size_ = {
    "name": "Garage størrelse",
    "type": "scalar",
    "description": "",
    "source": "BBR",
    "value": "garage_size",
}

prop_value_ = {
    "name": "Ejendomsværdi",
    "type": "scalar",
    "description": "Den seneste offentlige ejendomsvurdering.",
    "source": "SVUR",
    "value": "prop_value",
}

ground_value_ = {
    "name": "Grundværdi",
    "type": "scalar",
    "description": "Den seneste offentlige vurdering af grundværdien for ejendommen.",
    "source": "SVUR",
    "value": "ground_value",
}

domains = [
    size_,
    bis_area_,
    oth_area_,
    nr_rooms_,
    nr_baths_,
    nr_toilets_,
    total_area_,
    basement_area_,
    basement_area_used_,
    roof_area_,
    nr_of_floors_,
    out_room_size_,
    garage_size_,
    prop_value_,
    ground_value_,
]


def addDomains():
    for dom in domains:
        d = Domain(
            name=dom.get("name"),
            type=dom.get("type"),
            description=dom.get("description"),
            source=dom.get("source"),
            value=dom.get("value"),
        )
        d.save()

        # for v in dom.get('values'):
        #     c = Category(
        #         domain=d,
        #         name=v[0],
        #         value=v[1]
        #     )
        #     c.save()
