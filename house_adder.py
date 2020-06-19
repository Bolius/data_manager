import pandas as pd

from data_models.models import add_house


def addHouse():
    # load subscription data
    BBR = pd.read_csv("bbr.csv")[620902:]

    # loop for each municipality in subscription data
    for _, bbr in BBR.iterrows():
        # Get house object

        # print("Add house")
        # Make object

        add_house(bbr)
