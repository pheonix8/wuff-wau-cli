from pathlib import Path
from typing import Optional

import typer

import analytics

app = typer.Typer()
state = {"year": ""}


@app.callback()
def main(
    year: Optional[str] = typer.Option(
        None,
        "--year",
        "-y",
        help="Specify the deadline of the data, default is the current year.",
    ),
):
    """
    CLI app for the dog database of the city of Zurich.
    """
    if year is not None:
        state["year"] = year


@app.command()
def find(name: str):
    """
    Find all dogs with the given name and get their birth year and sex.
    """
    found_dogs = analytics.find_dogs_by_name(name, state["year"])

    print(f"Search for dogs by the name: {name}")

    print("==============")

    print(f"Found dogs:")
    for dog in found_dogs:
        print(f"{dog[0]} {dog[1]} {dog[2]}")


@app.command()
def stats():
    """
    Show some stats about the dogs of Zurich.

        - the longest names

        - the shortest names

        - the 10 most common names (male / female)

        - the dog count (male / female)
    """
    statistics = analytics.get_analytics(state["year"])

    print("Generate statistics for the current year")

    print("==============")

    print(f"longest dog name: {statistics['longestNames']}")
    print(f"shortest dog name: {statistics['shortestNames']}")

    print("--------------")

    print("Common names:")
    print(f"overall: {statistics['topTenCommonNames']['allNames']}")
    print(f"male: {statistics['topTenCommonNames']['allNamesM']}")
    print(f"female: {statistics['topTenCommonNames']['allNamesF']}")

    print("--------------")

    print(f"Dog count: {statistics['countOfDogs']['allCount']}")
    print(f"Males: {statistics['countOfDogs']['mCount']}")
    print(f"Females: {statistics['countOfDogs']['fCount']}")


@app.command()
def create(
    output_dir: Optional[str] = typer.Option(
        Path.cwd(),
        "--output-dir",
        "-o",
        help="Specify the output path for the dog image.",
    ),
):
    """
    Create a new dog based on the data of the city.

        - Random name

        - Random birth year

        - Random sex

        - Random picture from: 'https://random.dog'
    """
    if type(output_dir) == str:
        output_dir = Path(output_dir)
    new_dog = analytics.create_dog(output_dir, state["year"])

    print("Create new dog:")

    print("==============")

    print(f"Name: {new_dog['dogName']}")
    print(f"Birth year: {new_dog['dogBirth']}")
    print(f"Sex: {new_dog['dogSex']}")
    print(f"Image Path: {new_dog['dogImg']}")


if __name__ == '__main__':
    app()
