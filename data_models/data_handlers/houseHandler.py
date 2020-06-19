from data_models.data_handlers.api import kvhToBBR
from data_models.models import House

""" Takes a KVH calls the API and returns a house model """


def kvhToHouse(kvh, label="unkown"):
    data = kvhToBBR(kvh)
    bbr = data["bbr"]["values"]
    bbr["bld_reconyear"] = (
        bbr["bld_reconyear"]
        if bbr["bld_reconyear"] is None
        else bbr["bld_reconyear"].split("-")[0]
    )
    return House(
        address=bbr["acadr_name"],
        zipCode=int(bbr["pcode"]),
        size=int(bbr["unit_area_resi"]),
        type=bbr["unit_resityp_geo"],
        parish=int(bbr["parish"]) if bbr["parish"] is not None else int(bbr["pcode"]),
        ownership=bbr["unit_ownship"],
        geo_x=bbr["cell100_loc"]["x"],
        geo_y=bbr["cell100_loc"]["y"],
        heat_type=bbr["unit_nrg_heat"],
        build_year=bbr["bld_conyear"].split("-")[0],
        recon_year=bbr["bld_reconyear"],
        roof_type=bbr["bld_roof"],
        energy_type=bbr["unit_nrg_sup"],
        bis_area=bbr["unit_area_com"],
        oth_area=bbr["unit_area_oth"],
        nr_rooms=bbr["unit_rooms"],
        nr_baths=bbr["unit_rooms_bath"],
        nr_toilets=bbr["unit_rooms_toilet"],
        total_area=bbr["unit_area_total"],
        basement_area=bbr["bld_area_basement"],
        basement_area_used=bbr["floor_area_basmntlegl"],
        roof_area=bbr["floor_area_roofused"],
        nr_of_floors=bbr["bld_floors"],
        garage_size=bbr["bld_area_garage"],
        out_room_size=bbr["bld_area_consvtry"],
        heat1_type=bbr["bld_nrg_heat_instal"],
        heat2_type=bbr["bld_nrg_heat_instal2"],
        sup_heating=bbr["bld_nrg_heat_agent"],
        water_supply=bbr["bld_watersupl"],
        wal_material=bbr["bld_wallmatrl"],
        kvh=bbr["kvh"],
        prop_value=data["money"]["ejendomsvaerdi"],
        ground_value=data["money"]["grundvaerdi"],
        prop_type=data["money"]["ejendomstype"],
        energyLabel=label,
    )
