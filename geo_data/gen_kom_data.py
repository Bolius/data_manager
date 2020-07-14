import geojson
import geopandas as gpd
import pandas as pd
from numpy import array

kommuner = "kommuner.geojson"
befolkning = "kommunerBefolking.geojson"

with open(kommuner) as f:
    d = geojson.load(f)
    kom = d["features"]


d["features"] = kom[:10]
t = [(d["features"][i].properties["KOMNAVN"] == "Hedensted") for i in range(10)]

d["features"] = array(d["features"])[t]

test = list(
    set([d["features"][i].properties["KOMNAVN"] for i in range(len(d["features"]))])
)
df = gpd.GeoDataFrame(kom)


properties = gpd.GeoDataFrame(df["properties"].values.tolist(), index=df.index)
geometry = gpd.GeoDataFrame(df["geometry"].values.tolist(), index=df.index)

new_df = gpd.GeoDataFrame(pd.concat([geometry, properties], axis="columns"))
new_df.to_csv("kommuner.csv")
