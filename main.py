from pathlib import Path
import sys

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from typing import Optional
import typer

import analytics

console = Console()
error_console = Console(stderr=True, style="bold red")
app = typer.Typer()
state = {"year": None}


@app.callback()
def main(
    year: Optional[int] = typer.Option(
        None,
        "--year",
        "-y",
        help="Specify the deadline of the data, default uses the current year.",
    ),
) -> None:
    """
    CLI app for the dog database of the city of Zurich.
    """
    if year is not None:
        state["year"] = year


@app.command()
def find(name: str) -> None:
    """
    Find all dogs with the given name and get their birth year and sex.
    """
    if state["year"] is None:
        error_console.print("Using the data from the current year.", justify="center")

    console.print()
    console.print(f"# Searching for dogs with the name: {name} #", style="bold cyan")
    console.print()

    found_dogs = analytics.find_dogs_by_name(name, state["year"])

    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_column()
    grid.add_column()
    for dog in found_dogs:
        grid.add_row(f"[b cyan]{dog[0]}[/]", f"[b cyan]{dog[1]}[/]", f":{dog[2]}_sign:")

    dog_panel = Panel(grid, title=f"{len(found_dogs)} :dog: found with the name: {name}", style="bold green")

    console.print(dog_panel, justify="left")


@app.command()
def stats() -> None:
    """
    Show some stats about the dogs of Zurich.

        - the longest names

        - the shortest names

        - the 10 most common names (male / female)

        - the dog count (male / female)
    """
    if state["year"] is not None:
        year = f"year {state['year']}"
    else:
        year = "current year"

    console.print(f"# Loading statistics for the {year} #", style="bold cyan")
    console.print()

    statistics = analytics.get_analytics(state["year"])

    shortest_name_grid = Table(title="Shortest :dog: names", expand=True, show_header=False, style="green")
    shortest_name_grid.add_column(justify="center")
    for name in statistics.get('shortestNames'):
        shortest_name_grid.add_row(f"[cyan]- {name}[/cyan]")
    shortest_name_panel = Panel(shortest_name_grid)

    longest_name_grid = Table(title="Longest :dog: names", expand=True, show_header=False, style="green")
    longest_name_grid.add_column(justify="center")
    for name in statistics.get('longestNames'):
        longest_name_grid.add_row(f"[cyan]- {name}[/cyan]")
    longest_name_panel = Panel(longest_name_grid)

    common_table = Table(title="top 10 most common :dog: names", expand=True, style="green")
    common_table.add_column("All", style="white")
    common_table.add_column("Male :male_sign:", style="cyan")
    common_table.add_column("Female :female_sign:", style="violet")

    all_names = statistics.get('topTenCommonNames').get('allNames')
    all_names_m = statistics.get('topTenCommonNames').get('allNamesM')
    all_names_f = statistics.get('topTenCommonNames').get('allNamesF')

    for i in range(10):
        common_table.add_row(
            f"{all_names[i][0]}: {all_names[i][1]}",
            f"{all_names_m[i][0]}: {all_names_m[i][1]}",
            f"{all_names_f[i][0]}: {all_names_f[i][1]}"
        )

    common_name_panel = Panel(common_table)

    count_table = Table(title="Male :dog: vs Female :dog:", expand=True, style="green")
    count_table.add_column("Sex", style="cyan")
    count_table.add_column("Count", style="cyan")
    count_table.add_column("Percentage", style="cyan")

    total_count = statistics.get('countOfDogs').get('allCount')
    male_count = statistics.get('countOfDogs').get('mCount')
    female_count = statistics.get('countOfDogs').get('fCount')

    count_table.add_row(
        "Male :male_sign:",
        f"{statistics['countOfDogs']['mCount']}",
        f"{round(100 * male_count / total_count)} %",
    )
    count_table.add_row(
        "Female :female_sign:",
        f"{statistics['countOfDogs']['fCount']}",
        f"{round(100 * female_count / total_count)} %",
    )
    count_table.add_row(
        "Total",
        f"{statistics['countOfDogs']['allCount']}",
        f"100 %",
    )

    count_panel = Panel(count_table)

    statistics_layout = Layout()
    statistics_layout.split_row(
        Layout(shortest_name_panel),
        Layout(longest_name_panel),
        Layout(common_name_panel),
        Layout(count_panel),
    )

    console.print(f"Stats for the {year}", style="green bold", justify="center")
    console.print(statistics_layout)


@app.command()
def create(
        output_dir: Optional[str] = typer.Option(
            Path.cwd(),
            "--output-dir",
            "-o",
            help="Specify the output path for the dog image.",
        ),
) -> None:
    """
    Create a new dog based on the data of the city.

        - Random name

        - Random birth year

        - Random sex

        - Random picture from: 'https://random.dog'
    """
    if type(output_dir) == str:
        output_dir = Path(output_dir)

    if not output_dir.exists():
        error_console.print("This path does not exist set another path.")
        sys.exit(0)

    if state["year"] is None:
        error_console.print("Using the data from the current year.", justify="center")

    console.print(f"# Creating new dog #", style="bold cyan")
    console.print()

    new_dog = analytics.create_dog(output_dir, state["year"])

    new_dog_render = [
        f"[cyan]Name:        [/cyan][white]{new_dog.get('dogName')}[/white]",
        f"[cyan]Birth year:  [/cyan][white]{new_dog.get('dogBirth')}[/white]",
        f"[cyan]Sex:         [/cyan][white]{new_dog.get('dogSex')}[/white]",
        f"",
        f"[white]Find the dog image under the following path:[/white] [magenta]{new_dog.get('dogImg')}[/magenta]",
    ]

    dog_panel_panel = Panel('\n'.join(new_dog_render), title="New Dog :dog:", style="bold green")
    console.print(dog_panel_panel, justify="left")


if __name__ == '__main__':
    app()
