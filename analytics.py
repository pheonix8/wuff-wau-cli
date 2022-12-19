import collections
import random

import data


def find_dogs_by_name(name: str, year: str = ""):
    all_dogs = data.get_dog_data(year)
    filtered_dogs = []
    for dog in all_dogs:
        if dog["HundenameText"] == name:
            sex = 'm' if dog["SexHundSort"] == '1' else 'f'
            for i in range(int(dog["AnzHunde"])):
                filtered_dogs.append((
                    dog["HundenameText"],
                    dog["GebDatHundJahr"],
                    sex
                ))
    return filtered_dogs


def get_analytics(year: str = ""):
    all_dogs = data.get_dog_data(year)

    # Get the longest / shortest names
    max_length = max([len(row["HundenameText"]) for row in all_dogs])
    min_length = min([len(row["HundenameText"]) for row in all_dogs if row["HundenameText"] != "?"])

    # stats
    all_names_collection = collections.Counter([row["HundenameText"] for row in all_dogs])
    m_names_collection = collections.Counter([row["HundenameText"] for row in all_dogs if row["SexHundSort"] == "1"])
    f_names_collection = collections.Counter([row["HundenameText"] for row in all_dogs if row["SexHundSort"] == "2"])

    analytics = {
        "longestNames": list(
            row["HundenameText"] for row in all_dogs if len(row["HundenameText"]) == max_length
        ),
        "shortestNames": list(
            row["HundenameText"] for row in all_dogs if len(row["HundenameText"]) == min_length
        ),
        "topTenCommonNames": {
            "allNames": all_names_collection.most_common(10),
            "allNamesM": m_names_collection.most_common(10),
            "allNamesF": f_names_collection.most_common(10),
        },
        "countOfDogs": {
            "allCount": len([row for row in all_dogs]),
            "mCount": len([row for row in all_dogs if row["SexHundSort"] == "1"]),
            "fCount": len([row for row in all_dogs if row["SexHundSort"] == "2"]),

        }

    }

    return analytics


def create_dog(path: str, year: str = ""):
    all_dogs = data.get_dog_data(year)

    dog_name = random.choice([row["HundenameText"] for row in all_dogs])
    dog_age = random.choice([row["GebDatHundJahr"] for row in all_dogs])
    dog_image_path = f"{path}/{dog_name}_{dog_age}"
    generated_foto = data.get_random_dog(dog_image_path)

    new_dog = dict(dogName=dog_name, dogAge=dog_age, dogSex=random.choice(["m", "f"]), dogImg=generated_foto)

    return new_dog
