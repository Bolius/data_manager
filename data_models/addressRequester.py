import requests


class AddressRequester:
    def __init__(self, adgangs_adresse_id):
        self.id = adgangs_adresse_id

    def getKvh(self):
        url = "https://dawa.aws.dk/adgangsadresser"

        querystring = {"id": self.id}

        response = requests.request("GET", url, data="", params=querystring)
        return response.json()[0]["kvh"]
