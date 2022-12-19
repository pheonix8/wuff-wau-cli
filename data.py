import csv

import requests

ZUERICH_DOGS = "https://data.stadt-zuerich.ch/dataset/sid_stapo_hundenamen_od1002/download/KUL100OD1002.csv"
RANDOM_DOG_PICTURE = "https://random.dog/woof.json"


def get_dog_data(year: str = ""):
    response = requests.get(ZUERICH_DOGS)
    response.encoding = "utf-8-sig"
    split_output = response.text.splitlines()

    output_list = list(csv.DictReader(split_output))
    if year == "":
        year = output_list[-1].get("StichtagDatJahr")

    return [row for row in output_list if row["StichtagDatJahr"] == year]


def get_random_dog(path: str):
    response = requests.get(RANDOM_DOG_PICTURE)
    foto_url = response.json().get("url")

    while not foto_url.split(".")[-1].endswith(("jpg", "JPG", "jpeg", "JPEG")):
        response = requests.get(RANDOM_DOG_PICTURE)
        foto_url = response.json().get("url")

    ext = foto_url.split(".")[-1]
    path = f"{path}.{ext}"

    r = requests.get(foto_url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

    return path
