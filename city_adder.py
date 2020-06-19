import pandas as pd

from data_models.models import City, Municipality


def addCity():
    cities = pd.read_csv("cities.csv")

    for _, c in cities.iterrows():
        muni = Municipality.objects.get(municipality_name=c["municipality"])

        city = City(
            city_name=c["city"],
            zip_code_start=c["zip start"],
            zip_code_end=c["zip end"],
        )

        city.save()

        muni.cities.add(city)
