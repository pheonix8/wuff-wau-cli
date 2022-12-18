import collections
import random

import data


def find_dogs_by_name(name: str, year: str = ""):
    all_dogs = data.get_dog_data(year)
    filtered_dogs = []
    for dog in all_dogs:
        if dog["HundenameText"] == name:
            for i in range(int(dog["AnzHunde"])):
                filtered_dogs.append((
                    dog["HundenameText"],
                    dog["GebDatHundJahr"],
                    int(dog["SexHundSort"])
                ))
    return filtered_dogs
