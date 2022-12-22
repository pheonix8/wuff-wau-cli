# Wuff und Wau CLI

The aim of the project is to write a command-line tool which does various operations based on the [registered dogs in the city of Zurich](https://data.stadt-zuerich.ch/dataset/sid_stapo_hundenamen_od1002). This information is made available as "Open Data" and is thus freely accessible.

## Features

The CLI has three major features:

- Search for dogs using a given name
- Perform data analysis based on the entire data set
- Make up new dogs

### Help:
```
 Usage: wuff.py [OPTIONS] COMMAND [ARGS]...

 CLI app for the dog database of the city of Zurich.

╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --year                -y      INTEGER  Specify the deadline of the data, default uses the current year. [default: None]           │
│ --install-completion                   Install completion for the current shell.                                                  │
│ --show-completion                      Show completion for the current shell, to copy it or customize the installation.           │
│ --help                                 Show this message and exit.                                                                │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ create        Create a new dog based on the data of the city.                                                                     │
│ find          Find all dogs with the given name and get their birth year and sex.                                                 │
│ stats         Show some stats about the dogs of Zurich.                                                                           │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### 1. Search for dogs
```
 Usage: wuff.py find [OPTIONS] NAME

 Find all dogs with the given name and get their birth year and sex.

╭─ Arguments ─────────────────────────────────────────╮
│ *    name      TEXT  [default: None] [required]     │
╰─────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────╮
│ --help          Show this message and exit.         │
╰─────────────────────────────────────────────────────╯
```

#### Examples:
```
python wuff.py find John
```
```
python wuff.py --year 2015 find John
```

#### Output:
```
╭─ 5 🐶 found with the name: John ─╮
│ John           2009          ♂   │
│ John           2011          ♂   │
│ John           2014          ♂   │
│ John           2020          ♂   │
│ John           2021          ♂   │
╰──────────────────────────────────╯
```

### 2. Load statistics of the year
```
  Usage: wuff.py stats [OPTIONS]

 Show some stats about the dogs of Zurich.
 - the longest names
 - the shortest names
 - the 10 most common names (male / female)
 - the dog count (male / female)

╭─ Options ───────────────────────────────────────╮
│ --help          Show this message and exit.     │
╰─────────────────────────────────────────────────╯
```

#### Examples:
```
python wuff.py stats
```
```
python wuff.py --year 2015 stats
```

#### Output:
```
╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────── Stats for the year 2015 ────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ ╭─────────────────────╮╭─────────────────────────────────────────────────────────────────────────╮╭──────────────────────────────────────────────────────────────────────────────╮╭──────────────────────────────────────────────────────────────────╮ │
│ │  Shortest 🐶 names  ││                            Longest 🐶 names                            ││                         top 10 most common 🐶 names                          ││                       Male 🐶 vs Female 🐶                      │ │
│ │ ┌─────────────────┐ ││ ┌─────────────────────────────────────────────────────────────────────┐ ││ ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓ ││ ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓ │ │
│ │ │      - Bo       │ ││ │                  - (Karl) Kaiser Karl vom Edersee                   │ ││ ┃ All                     ┃ Male ♂                  ┃ Female ♀             ┃ ││ ┃ Sex                 ┃ Count         ┃ Percentage             ┃ │ │
│ │ │      - Bo       │ ││ │                  - Ahab v. Pirateprincessbulldogs                   │ ││ ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩ ││ ┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩ │ │
│ │ │      - DJ       │ ││ │                  - Akando-Abucco v. Ritters Glück                   │ ││ │ Luna: 95                │ Rocky: 41               │ Luna: 95             │ ││ │ Male ♂              │ 3432          │ 49 %                   │ │ │
│ │ │      - Jo       │ ││ │                  - Amazing Adel. fr.Sands.(Bonita                   │ ││ │ Rocky: 42               │ Lucky: 31               │ Kira: 27             │ ││ │ Female ♀            │ 3548          │ 51 %                   │ │ │
│ │ │      - Lu       │ ││ │                  - Berenice v. Happy Morning Star                   │ ││ │ Lucky: 35               │ Leo: 29                 │ Lola: 25             │ ││ │ Total               │ 6980          │ 100 %                  │ │ │
│ │ │      - Mo       │ ││ │                  - Black Hamlet B For Blueberry H                   │ ││ │ Leo: 30                 │ Max: 27                 │ Bella: 23            │ ││ └─────────────────────┴───────────────┴────────────────────────┘ │ │
│ │ │      - Mo       │ ││ │                  - Cody (Captain Luka High Hopes)                   │ ││ │ Kira: 27                │ Charly: 22              │ Gina: 22             │ │╰──────────────────────────────────────────────────────────────────╯ │
│ │ │      - Mo       │ ││ │                  - Cézanne Anuk Etoile des filous                   │ ││ │ Max: 27                 │ Snoopy: 22              │ Lucy: 21             │ │                                                                     │
│ │ │      - Mu       │ ││ │                  - Daisy  Desirée Rainerschlössel                   │ ││ │ Lola: 25                │ Chico: 19               │ Mia: 20              │ │                                                                     │
│ │ │      - Su       │ ││ │                  - Definitley Maybe Abs. Charming                   │ ││ │ Bella: 23               │ Jack: 19                │ Daisy: 19            │ │                                                                     │
│ │ │      - Té       │ ││ │                  - Everest First Sir John, Bonito                   │ ││ │ Snoopy: 23              │ Paco: 19                │ Emma: 18             │ │                                                                     │
│ │ └─────────────────┘ ││ │                  - Felix (Candyboy v. alten Zoll)                   │ ││ │ Charly: 22              │ Blacky: 17              │ Nina: 18             │ │                                                                     │
│ ╰─────────────────────╯│ │                  - Flo(Royal von Prince of Wales)                   │ ││ └─────────────────────────┴─────────────────────────┴──────────────────────┘ │                                                                     │
│                        │ │                  # ... more output omitted ...                      │ │╰──────────────────────────────────────────────────────────────────────────────╯                                                                     │
│                        │ └─────────────────────────────────────────────────────────────────────┘ │                                                                                                                                                     │
│                        ╰─────────────────────────────────────────────────────────────────────────╯                                                                                                                                                     │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### 3. Create a random dog from the data
```
 Usage: wuff.py create [OPTIONS]

 Create a new dog based on the data of the city.
 - Random name
 - Random birth year
 - Random sex
 - Random picture from: 'https://random.dog'

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --output-dir  -o      TEXT  Specify the output path for the dog image. [default: C:\Users\Leo Oetterli\PycharmProjects\WuffWauCLI]     │
│ --help                      Show this message and exit.                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### Examples:
```
python wuff.py create
```
```
python wuff.py --year 2015 create
```
```
python wuff.py create --output-dir '/home/pheonix8/downloads'
```

#### Output:
```
╭──────────────────────────────────── New Dog 🐶 ────────────────────────────────────╮
│ Name:        Zoe                                                                   │
│ Birth year:  2014                                                                  │
│ Sex:         f                                                                     │
│                                                                                    │
│ Find the dog image under the following path: /home/pheonix8/downloads/Zoe_2014.jpg │
╰────────────────────────────────────────────────────────────────────────────────────╯
```