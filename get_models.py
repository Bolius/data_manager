import os
import zipfile

import requests


class ModelFetcher:
    """
    Takes model names and checks whether the zip file with the name modelName.zip
    is in the google cloud bucket.
    If it is newer, or if it dosn't exsists locally, it gets the zip file and
    extracts it.
    """

    def __init__(self, models):
        if not os.path.exists(self.working_dir):
            os.makedirs("ai_models")

        self.models = models
        self._checkModels()

    working_dir = "ai_models"

    def _shouldGetModel(self, modelName):
        dest_folder = os.path.join(self.working_dir, modelName)
        return not os.path.exists(dest_folder)

    def _getModel(self, modelName):
        print("Downloading model File")
        response = requests.get(
            f"https://storage.googleapis.com/bolius-ml-models/{modelName}.zip"
        )
        if response.status_code != 200:
            raise ConnectionError("Could not get zip file")

        zipDest = os.path.join(self.working_dir, f"{modelName}.zip")
        with open(zipDest, "wb+") as zip:
            zip.write(response.content)

        ref = zipfile.ZipFile(zipDest, "r")
        ref.extractall(self.working_dir)
        ref.close()
        os.remove(zipDest)

    def _checkModels(self):
        for model in self.models:
            if self._shouldGetModel(model):
                print(f"Getting model {model}")
                self._getModel(model)


ModelFetcher(["energy", "komfort", "proposals", "radon"])
