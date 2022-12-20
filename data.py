import csv
from pathlib import Path
import sys
from typing import Dict, List


import requests
from rich.console import Console
from rich.panel import Panel

ZUERICH_DOGS = "https://data.stadt-zuerich.ch/dataset/sid_stapo_hundenamen_od1002/download/KUL100OD1002.csv"
RANDOM_DOG_PICTURE = "https://random.dog/woof.json"
DOG_DATA = List[Dict[str, str]]
error_console = Console(stderr=True, style="bold red")


def get_dog_data(year: int) -> DOG_DATA:
    """
    Gets a dataset of the Zurich police department with all registered dogs in the city of Zurich.
    The given year is the deadline of the data, no year given returns the newest data available.

            Parameters:
                year        (str): Deadline of the data. [Default] ""

            Returns:
                dog_data    (list): Dataset containing Dictionary entries for the dogs.
    """
    # request data
    try:
        response = requests.get(ZUERICH_DOGS)
        response.raise_for_status()
    except requests.RequestException as e:
        error_console.print(f"The request threw a:\n{e}\nPlease check your internet, or contact "
                            f"the developer.")
        sys.exit(1)
    response.encoding = "utf-8-sig"
    split_output = response.text.splitlines()
    # read csv file
    output_list = list(csv.DictReader(split_output))
    # set current year if year is ""
    if year is None:
        year = int(output_list[-1].get("StichtagDatJahr"))
    # extract the data at a specific date
    dog_data = list(row for row in output_list if row.get('StichtagDatJahr') == str(year))
    # check if the given year is in the data
    if len(dog_data) == 0:
        years = sorted(set(list(f"{row.get('StichtagDatJahr')}" for row in output_list)))
        error_console.print(Panel('\n'.join(years), title=f"The given year does not exist in the data, try one of the "
                                                          f"following years:"))
        sys.exit(0)
    else:
        return dog_data


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
    try:
        response = requests.get(RANDOM_DOG_PICTURE)
    except requests.RequestException as e:
        error_console.print(f"The request threw a:\n{e}\nPlease check your internet, or contact "
                            f"the developer.")
        sys.exit(1)
    foto_url = response.json().get("url")
    # check that the url is a JPEG
    while not foto_url.split(".")[-1].endswith(("jpg", "JPG", "jpeg", "JPEG")):
        try:
            response = requests.get(RANDOM_DOG_PICTURE)
        except requests.RequestException as e:
            error_console.print(f"The request threw a:\n{e}\nPlease check your internet, or contact "
                                f"the developer.")
            sys.exit(1)
        foto_url = response.json().get("url")
    # get the extension and create the path
    ext = foto_url.split(".")[-1]
    output_path = output_path / f"{name}.{ext}"
    # request the picture and save it into the given path
    try:
        r = requests.get(foto_url, stream=True)
    except requests.RequestException as e:
        error_console.print(f"The request threw a:\n{e}\nPlease check your internet, or contact "
                            f"the developer.")
        sys.exit(1)
    if r.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

    return str(output_path)
