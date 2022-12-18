import csv

import requests

ZUERICH_DOGS = "https://data.stadt-zuerich.ch/dataset/sid_stapo_hundenamen_od1002/download/KUL100OD1002.csv"


def get_dog_data(year: str = ""):
    response = requests.get(ZUERICH_DOGS)
    response.encoding = "utf-8-sig"
    split_output = response.text.splitlines()

    output_list = list(csv.DictReader(split_output))
    if year == "":
        year = output_list[-1].get("StichtagDatJahr")

    return [row for row in output_list if row["StichtagDatJahr"] == year]
