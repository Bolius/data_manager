import geopandas as geo_pd
import pandas as pd
from radon_notebooks.data_processing import one_hot_encode
from shapely.geometry import Point
from sklearn.externals import joblib


class RadonPredicter:
    def __init__(self):
        base = "./ai_models/radon/"
        gt_path = base + "soilTypes25000/Jordart_25000_reduced.shp"
        geo_data = geo_pd.read_file(gt_path)
        bounds = geo_data.geometry.bounds

        self.geo_data = geo_data
        self.bounds = bounds

        self.ground_type = pd.concat([geo_data, bounds], axis=1)
        self.clf = joblib.load(base + "model.pkl")
        print("radon predictor loaded")

    def computeSoil(self, bbr):
        px = bbr.x
        py = bbr.y
        # Get soil type house area
        geo_data = self.geo_data
        ground_type = self.ground_type

        geo_data_reduced = ground_type[ground_type["minx"] <= px]
        geo_data_reduced = geo_data_reduced[geo_data_reduced["maxx"] > px]
        geo_data_reduced = geo_data_reduced[geo_data_reduced["miny"] <= py]
        geo_data_reduced = geo_data_reduced[geo_data_reduced["maxy"] > py]
        geo_data_reduced = geo_data_reduced["minx"] - px

        closest = abs(geo_data_reduced).sort_values().index

        p = Point([px, py])
        soil_idx = "unknown"

        for type in closest:
            if geo_data.loc[type].geometry.contains(p):
                soil_idx = type

        if soil_idx == "unknown":
            raise ValueError("No soil type found")

        soil = geo_data.loc[soil_idx]["JSYM1"]

        return soil

    def predictParams(self, bbr, soil):
        # One hot encoding of categorical data
        wall_material = one_hot_encode("wall_material", bbr.wall_material)
        nrg_heat = one_hot_encode("nrg_heat", bbr.nrg_heat)
        ground_type = one_hot_encode("ground_type", soil)

        X = [
            [
                bbr.has_basement,
                bbr.nr_floors,
                bbr.build_year,
                bbr.rebuild_year,
                bbr.x,
                bbr.y,
                bbr.ground_size,
                bbr.size,
                bbr.roof_area,
                bbr.basement_area,
            ]
            + wall_material
            + nrg_heat
            + ground_type
        ]

        # Predict Bq
        bqm3 = self.clf.predict(X)
        return bqm3
