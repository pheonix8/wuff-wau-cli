import collections
from pathlib import Path
import random

import data

DOG_DATA = list[tuple[str, str, str]]
ANALYTICS_DATA = dict[
    str, list[str],
    str, dict[str, list[str]]
]
NEW_DOG_DATA = dict[str, str]


def find_dogs_by_name(name: str, year: str = "") -> DOG_DATA:
    """
    Filter a dog list to only contain the dogs with a specific name

            Parameters:
                name            (str): Name of the dog which should be searched.
                year            (str): Year for the deadline of the data. [Default] ""

            Returns:
                filtered_dogs   (list): Filtered dogs (name,birthYear,sex)
    """
    # get a dog list
    all_dogs = covert_dog_dataset(data.get_dog_data(year))
    # filter the list  for the given name
    filtered_dogs = [dog for dog in all_dogs if dog[0] == name]

    return filtered_dogs


def get_analytics(year: str = "") -> ANALYTICS_DATA:
    """
    Analyses a dog list and finds:

        - the longest names
        - the shortest names
        - the top ten most common names (Male / Female)
        - the count of dogs (Male / Female)

            Parameters:
                year            (str): Year for the deadline of the data. [Default] ""

            Returns:
                analytics   (dict): The mentioned analytics of the dog list
    """
    # get a dog list
    all_dogs = covert_dog_dataset(data.get_dog_data(year))
    # filter out the names into lists
    all_names = [dog[0] for dog in all_dogs]
    m_names = [dog[0] for dog in all_dogs if dog[2] == "m"]
    f_names = [dog[0] for dog in all_dogs if dog[2] == "f"]
    # Get the longest / shortest names
    max_length = max([len(dog) for dog in all_names])
    min_length = min([len(dog) for dog in all_names if dog != "?"])

    analytics = {
        "longestNames": list(
            dog[0] for dog in all_dogs if len(dog[0]) == max_length
        ),
        "shortestNames": list(
            dog[0] for dog in all_dogs if len(dog[0]) == min_length
        ),
        "topTenCommonNames": {
            "allNames": collections.Counter(all_names).most_common(10),
            "allNamesM": collections.Counter(m_names).most_common(10),
            "allNamesF": collections.Counter(f_names).most_common(10),
        },
        "countOfDogs": {
            "allCount": len(all_names),
            "mCount": len(m_names),
            "fCount": len(f_names),

        }

    }

    return analytics


def create_dog(output_path: Path, year: str = "") -> NEW_DOG_DATA:
    """
    Creates a new dog based on a dog list

        - Random name
        - Random birth year
        - Random sex
        - Random dog image from https://random.dog

            Parameters:
                output_path (Path): Path to which the image should be saved.
                year            (str): Year for the deadline of the data. [Default] ""

            Returns:
                new_dog   (dict): The mentioned new dog
    """
    # get a dog list
    all_dogs = covert_dog_dataset(data.get_dog_data(year))
    # filter out the necessary info and get a random item
    dog_name = random.choice([dog[0] for dog in all_dogs])
    dog_birth = random.choice([dog[1] for dog in all_dogs])
    # get a random dog image downloaded
    generated_foto = data.get_random_dog(output_path, f"{dog_name}_{dog_birth}")

    new_dog = dict(
        dogName=dog_name,
        dogBirth=dog_birth,
        dogSex=random.choice(["m", "f"]),
        dogImg=generated_foto
    )

    return new_dog


def covert_dog_dataset(dog_data: data.DOG_DATA) -> DOG_DATA:
    """
    Filter a dog list to only contain the dogs with a specific name

            Parameters:
                dog_data    (list): List of dictionaries {HundenameText,GebDatHundJahr,SexHundSort,AnzHunde}

            Returns:
                all_dogs    (list): List of dogs (name,birthYear,sex)
    """
    all_dogs = []
    # loop through the dog data and only save the important values into a tuple
    for dog in dog_data:
        # convert the Sex value into a useful character
        if dog["SexHundSort"] == '1':
            sex = 'm'
        elif dog["SexHundSort"] == '2':
            sex = 'f'
        else:
            sex = "?"
        for i in range(int(dog["AnzHunde"])):
            all_dogs.append((
                dog["HundenameText"],
                dog["GebDatHundJahr"],
                sex
            ))

    return all_dogs
