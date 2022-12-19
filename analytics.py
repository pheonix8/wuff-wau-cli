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
            "all_names": all_names_collection.most_common(10),
            "all_names_m": m_names_collection.most_common(10),
            "all_names_f": f_names_collection.most_common(10),
        },
        "countOfDogs": {
            "all_count": len([row for row in all_dogs]),
            "m_count": len([row for row in all_dogs if row["SexHundSort"] == "1"]),
            "f_count": len([row for row in all_dogs if row["SexHundSort"] == "2"]),

        }

    }

    return analytics
