import collections
from pathlib import Path
import random

import data


def find_dogs_by_name(name: str, year: str = ""):
    all_dogs = get_all_dogs(data.get_dog_data(year))

    filtered_dogs = [dog for dog in all_dogs if dog[0] == name]

    return filtered_dogs


def get_analytics(year: str = ""):
    all_dogs = get_all_dogs(data.get_dog_data(year))

    # Name lists
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


def create_dog(output_path: Path, year: str = ""):
    all_dogs = get_all_dogs(data.get_dog_data(year))

    dog_name = random.choice([dog[0] for dog in all_dogs])
    dog_birth = random.choice([dog[1] for dog in all_dogs])
    generated_foto = data.get_random_dog(output_path, f"{dog_name}_{dog_birth}")

    new_dog = dict(
        dogName=dog_name,
        dogBirth=dog_birth,
        dogSex=random.choice(["m", "f"]),
        dogImg=generated_foto
    )

    return new_dog


def get_all_dogs(dog_data: list):
    all_dogs = []

    for dog in dog_data:
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
