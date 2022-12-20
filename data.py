import csv
from pathlib import Path

import requests

ZUERICH_DOGS = "https://data.stadt-zuerich.ch/dataset/sid_stapo_hundenamen_od1002/download/KUL100OD1002.csv"
RANDOM_DOG_PICTURE = "https://random.dog/woof.json"
DOG_DATA = list[dict[str, str]]


def get_dog_data(year: str = "") -> DOG_DATA:
    """
    Gets a dataset of the Zurich police department with all registered dogs in the city of Zurich.
    The given year is the deadline of the data, no year given returns the newest data available.

            Parameters:
                year        (str): Deadline of the data. [Default] ""

            Returns:
                dog_data    (list): Dataset containing Dictionary entries for the dogs.
    """
    # request data
    response = requests.get(ZUERICH_DOGS)
    response.encoding = "utf-8-sig"
    split_output = response.text.splitlines()
    # read csv file
    output_list = list(csv.DictReader(split_output))
    # set current year if year is ""
    if year == "":
        year = output_list[-1].get("StichtagDatJahr")
    # return the read data at a specific date
    return [row for row in output_list if row["StichtagDatJahr"] == year]


def get_random_dog(output_path: Path, name: str) -> str:
    """
    Downloads an image from https//random.dog to the given destination, if it's a JPEG.

            Parameters:
                output_path (Path): Path to which the image should be saved.
                name        (str): Name of the image.

            Returns:
                output_path (str): Full path to the saved image.
    """
    # request a picture url
    response = requests.get(RANDOM_DOG_PICTURE)
    foto_url = response.json().get("url")
    # check that the url is a JPEG
    while not foto_url.split(".")[-1].endswith(("jpg", "JPG", "jpeg", "JPEG")):
        response = requests.get(RANDOM_DOG_PICTURE)
        foto_url = response.json().get("url")
    # get the extension and create the path
    ext = foto_url.split(".")[-1]
    output_path = output_path / f"{name}.{ext}"
    # request the picture and save it into the given path
    r = requests.get(foto_url, stream=True)
    if r.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

    return str(output_path)
