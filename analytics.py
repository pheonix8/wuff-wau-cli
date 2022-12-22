from __future__ import annotations

import collections
import shutil
from pathlib import Path
import random
import sys
from typing import Any

from PIL import Image
from rich.console import Console

import data

error_console = Console(stderr=True, style="bold red")


def find_dogs_by_name(name: str, year: int | None) -> list[tuple[str, str, str]]:
    """
    Filter a dog list to only contain the dogs with a specific name.

            Parameters:
                name            (str): Name of the dog which should be searched.
                year            (str): Year for the deadline of the data.

            Returns:
                filtered_dogs   (list): Filtered dogs (name,birthYear,sex)
    """
    # get a dog list.
    all_dogs = convert_dog_dataset(data.get_dog_data(year))
    # filter the list  for the given name.
    filtered_dogs = list(dog for dog in all_dogs if dog[0] == name)
    # check if a dog was found with the given name.
    if len(filtered_dogs) == 0:
        error_console.print(f"The dog {name} was not found in the data.")
        sys.exit(0)

    return filtered_dogs


def get_analytics(year: int | None) -> dict[str, list[str] | dict[str, list[tuple[str, int]]] | dict[str, int]]:
    """
    Analyses a dog list and finds:

        - the longest names
        - the shortest names
        - the top ten most common names (Male / Female)
        - the count of dogs (Male / Female)

            Parameters:
                year            (str): Year for the deadline of the data.

            Returns:
                analytics   (dict): The newly created statistics.
    """
    # get a dog list.
    all_dogs = convert_dog_dataset(data.get_dog_data(year))
    # filter out the names into lists.
    all_names = list(dog[0] for dog in all_dogs)
    m_names = list(dog[0] for dog in all_dogs if dog[2] == "male")
    f_names = list(dog[0] for dog in all_dogs if dog[2] == "female")
    # Get the longest / shortest names.
    max_length = max(list(len(dog) for dog in all_names))
    min_length = min(list(len(dog) for dog in all_names if dog != "?"))
    # create the analytics dictionary.
    analytics = dict(
        longestNames=list(
            dog[0] for dog in all_dogs if len(dog[0]) == max_length
        ),
        shortestNames=list(
            dog[0] for dog in all_dogs if len(dog[0]) == min_length
        ),
        topTenCommonNames=dict(
            allNames=collections.Counter(all_names).most_common(10),
            allNamesM=collections.Counter(m_names).most_common(10),
            allNamesF=collections.Counter(f_names).most_common(10),
        ),
        countOfDogs=dict(
            allCount=len(all_names),
            mCount=len(m_names),
            fCount=len(f_names),

        ),

    )

    return analytics


def create_dog(output_path: Path, year: int | None) -> dict[str, str]:
    """
    Creates a new dog based on a dog list.

        - Random name
        - Random birth year
        - Random sex
        - Random dog image from https://random.dog

            Parameters:
                output_path (Path): Path to which the image should be saved.
                year            (str): Year for the deadline of the data.

            Returns:
                new_dog   (dict): The newly created Dog.
    """
    # get a dog list.
    all_dogs = convert_dog_dataset(data.get_dog_data(year))
    # filter out the necessary info and get a random item.
    dog_name = random.choice(list(dog[0] for dog in all_dogs))
    dog_birth = random.choice(list(dog[1] for dog in all_dogs))
    # get a random dog image downloaded.
    generated_foto = stitch_images(output_path, f"{dog_name}_{dog_birth}")
    # create a dog dictionary.
    new_dog = dict(
        dogName=dog_name,
        dogBirth=dog_birth,
        dogSex=random.choice(["m", "f"]),
        dogImg=generated_foto
    )

    return new_dog


def convert_dog_dataset(dog_data: list[dict[str, str]]) -> list[tuple[str, str, str]]:
    """
    Convert the dog dataset to a list of tuples.

            Parameters:
                dog_data    (list): List of dictionaries, {HundenameText,GebDatHundJahr,SexHundSort,AnzHunde}

            Returns:
                all_dogs    (list): List of dogs, (name,birthYear,sex)
    """
    all_dogs = list()
    # loop through the dog data and only save the important values into a tuple.
    for dog in dog_data:
        # convert the Sex value into a useful character.
        if dog.get('SexHundSort') == '1':
            sex = 'male'
        elif dog.get('SexHundSort') == '2':
            sex = 'female'
        else:
            sex = "?"
        for i in range(int(dog.get('AnzHunde'))):
            all_dogs.append((
                dog.get('HundenameText'),
                dog.get('GebDatHundJahr'),
                sex
            ))

    return all_dogs


def stitch_images(output_path: Path, name: str) -> str:
    """
    Stitches two random dog images together and save the new image at the given path.

            Parameters:
                output_path (Path): Path to which the image should be saved.
                name        (str): Name of the image.

            Returns:
                 output_path (str): Path to which the image should be saved.
    """
    # creating a temporary folder
    temp_path = Path.cwd() / "tmp"
    temp_path.mkdir()
    # get two dog images.
    temp_img_1_path = data.get_random_dog(temp_path, "temp_1")
    temp_img_2_path = data.get_random_dog(temp_path, "temp_2")
    temp_img_1 = Image.open(temp_img_1_path)
    temp_img_2 = Image.open(temp_img_2_path)
    # get the combined width and maximal height of the images.
    new_width = temp_img_1.size[0] + temp_img_2.size[0]
    new_height = temp_img_1.size[1] if temp_img_1.size[1] >= temp_img_2.size[1] else temp_img_2.size[1]
    # creat a new image.
    new_dog_image = Image.new('RGB', (new_width, new_height), "white")
    # paste the dog images into the new image and save it.
    new_dog_image.paste(temp_img_1, (0, 0))
    new_dog_image.paste(temp_img_2, (temp_img_1.size[0], 0))
    new_dog_image.save(str(output_path / f"{name}.jpg"))
    # removing the temporary folder and files
    shutil.rmtree(temp_path)

    return str(output_path / f"{name}.jpg")
