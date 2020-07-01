import graphene
from data_models.geomatic.bbr import getBBRInfo
from data_models.geomatic.mappings import unit_resityp_geo_map, unit_usage_v2_map

# from .water_risk import WaterRisk
from .bbr_info import BBRInfo
from .radon import Radon

# from data_models.radonPredicter import RadonPredicter
# from data_models.views.radon_views import radonPred


class House(graphene.ObjectType):
    addressInput = graphene.String(required=False)
    kvhxInput = graphene.String(required=False)
    #    water_risk = graphene.NonNull(WaterRisk)
    bbr_info = graphene.NonNull(BBRInfo)
    radon = graphene.NonNull(Radon)

    def resolve_bbr_info(parent, info):
        if parent.kvhxInput is not None:
            geo_data = getBBRInfo(kvhx=parent.kvhxInput)
            geo_xy = getBBRInfo(kvhx=parent.kvhxInput, coords="xy")
        else:
            geo_data = getBBRInfo(address=parent.addressInput)
            geo_xy = getBBRInfo(address=parent.addressInput, coords="xy")

        bld_usage = [
            cat["name"]
            for cat in unit_usage_v2_map
            if geo_data["bld_usage_v2"] == cat["self"]["id"]
        ][0]

        unit_resityp_geo = [
            cat["name"]
            for cat in unit_resityp_geo_map
            if geo_data["unit_resityp_geo"] == cat["self"]["id"]
        ][0]

        return BBRInfo(
            bbr_id=geo_data["unadr_bbrid"],
            address=geo_data["acadr_name"],
            kvhx=geo_data["kvhx_dawa"],
            size=geo_data["bld_area_resi"],
            ground_size=geo_data["bld_area_total"]
            if geo_data["bld_area_total"] is not None
            else geo_data["bld_area_resi"],
            type=bld_usage,
            build_year=int(geo_data["bld_conyear"].split("-")[0]),
            rebuild_year=int(geo_data["bld_reconyear"].split("-")[0])
            if geo_data["bld_reconyear"] is not None
            else int(geo_data["bld_conyear"].split("-")[0]),
            nr_floors=geo_data["bld_floors"],
            prop_type=unit_resityp_geo,
            has_basement=geo_data["bld_area_basement"] is not None,
            basement_area=geo_data["bld_area_basement"]
            if geo_data["bld_area_basement"] is not None
            else 0,
            roof_area=geo_data["bld_area_roof"]
            if geo_data["bld_area_roof"] is not None
            else 0,
            wall_material=geo_data["bld_wallmatrl"],
            nrg_heat=geo_data["unit_nrg_heat"],
            lat=round(geo_data["acadr_loc"]["lat"], 8),
            long=round(geo_data["acadr_loc"]["long"], 8),
            x=round(geo_xy["acadr_loc"]["x"], 8),
            y=round(geo_xy["acadr_loc"]["y"], 8),
        )

    #
    # def resolve_water_risk(parent, info):
    #     bbr_info = parent.resolve_bbr_info(info)
    #     return WaterRisk(address=bbr_info.address, id=bbr_info.bbr_id)

    # def resolve_radon(parent, info):
    #     bbr = parent.resolve_bbr_info(info)
    #     soil = radonPred.computeSoil(bbr)
    #     bq = radonPred.predictParams(bbr, soil)
    #     return Radon(bqm3=bq, soil_type=soil)
