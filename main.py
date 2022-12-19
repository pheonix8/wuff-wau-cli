import typer

import analytics

app = typer.Typer()


@app.command()
def find(name: str):
    found_dogs = analytics.find_dogs_by_name(name)

    print(f"Search for dogs by the name: {name}")

    print("==============")

    print(f"Found dogs:")
    for dog in found_dogs:
        print(f"{dog[0]} {dog[1]} {dog[2]}")



@app.command()
def stats():
    statistics = analytics.get_analytics()

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
def create():
    new_dog = analytics.create_dog()

    print("Create new dog:")

    print("==============")

    print(f"Name: {new_dog['dogName']}")
    print(f"Age: {new_dog['dogAge']}")
    print(f"Sex: {new_dog['dogSex']}")
    print(f"Image Path: {new_dog['dogImg']}")


if __name__ == '__main__':
    app()
