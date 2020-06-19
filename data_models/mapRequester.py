import requests
from pyproj import Proj


class MapRequester:
    def __init__(
        self,
        x,
        y,
        espg="EPSG:25832",
        x_diff=0.0017800349412893217,
        y_diff=0.0008891840047351555,
    ):
        self.espg = espg
        self.x = x
        self.y = y
        self.x_diff = x_diff
        self.y_diff = y_diff

    def getBoundingBox(self):
        p = Proj(init=self.espg)
        mins = p(self.x - self.x_diff, self.y - self.y_diff)
        maxs = p(self.x + self.x_diff, self.y + self.y_diff)
        return f"{mins[0]},{mins[1]},{maxs[0]},{maxs[1]}"

    def getShadow(self):
        return self.imgKortforsyningen("dhm", "dhm_nedboer_skyggekort", mode="L")

    def getSurface(self):
        return self.imgKortforsyningen("dhm", "dhm_overflade", mode="1")

    def getBlueSpot(self):
        return self.imgKortforsyningen(
            "dhm",
            "dhm_bluespot_ekstremregn",
            styles="bluespot_ekstremregn_0_015",
            mode="RGB",
        )

    def getMat(self):
        return self.imgKortforsyningen("mat", "MatrikelSkel", mode="RGB")

    def imgKortforsyningen(self, service, model, styles="", mode="1"):
        url = "https://kortforsyningen.kms.dk/"
        querystring = {
            "service": "WMS",
            "login": "rotendahl",
            "password": "tLZHWLMo>vg26Ad",
            "servicename": service,  # "building_inspire",
            "LAYERS": model,  # "BU.Building",
            "TRANSPARENT": "True",
            "VERSION": "1.1.1",
            "REQUEST": "GetMap",
            "FORMAT": "image/png",
            "SRS": "EPSG:25832",
            "BBOX": self.getBoundingBox(),
            "WIDTH": "400",
            "HEIGHT": "400",
        }
        if len(styles) > 0:
            querystring["styles"] = styles

        response = requests.request("GET", url, data="", params=querystring)
        return response.url
