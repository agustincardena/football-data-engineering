# Football Data Engineering

Data engineering project focused on collecting, validating, transforming and storing Argentine football data using Python and PostgreSQL.

The project uses the 2026 Liga Profesional Clausura as the main dataset. The resulting dataset is structured for analytical queries and future visualization.

## Project Goal

Build a data pipeline that collects football match data from external sources, processes and validates it with Python, and stores the final dataset in PostgreSQL.

The project focuses on:

* Python
* SQL
* PostgreSQL
* Data cleaning and validation
* ETL pipelines
* Data reconciliation
* Relational database design
* Data engineering concepts

The long-term goal is to use the structured data for football performance analysis and visualization.

## Tech Stack

* Python 3
* PostgreSQL
* psycopg
* Requests
* JSON
* Git / GitHub

## Pipeline

```text
External sources
       ↓
Python extraction
       ↓
Data cleaning and transformation
       ↓
Data validation
       ↓
PostgreSQL
       ↓
SQL analytics
       ↓
Power BI
```

Future improvements will include automated and incremental data updates.

## Project Structure

```text
Football-Data-Engineering/

├── src/
│   ├── compare_jornada1.py
│   ├── database.py
│   ├── extract.py
│   ├── extract_historical.py
│   ├── get_matches.py
│   ├── get_rounds.py
│   ├── get_teams.py
│   └── validation.py
│
├── flashscore_historical.json
├── matches.json
├── .gitignore
└── README.md
```

The `.env` file is used locally for database credentials and is excluded from Git.

## Data Extraction

The main extraction process uses Soccerway data.

`extract.py`:

1. Requests the source page.
2. Extracts the match blocks from the response.
3. Extracts:

   * Match ID
   * Date
   * Round
   * Home team
   * Away team
   * Home score
   * Away score
4. Removes duplicate matches.
5. Sorts matches by date.
6. Saves the extracted data to `matches.json`.

The data is stored as JSON before being loaded into PostgreSQL.

## Data Validation

Before loading the data into PostgreSQL, `validation.py` checks the dataset for common data quality problems.

The validation process checks:

* Duplicate IDs
* Missing required fields
* Matches with and without results
* Matches without results that have a past date
* Number of matches per round

This helps detect incomplete or inconsistent data before loading it into the database.

## Historical Data Recovery

During the project, the Soccerway results page did not return all historical matches directly.

The initial extraction resulted in incomplete data for Jornada 1.

To recover the missing matches, a Flashscore historical feed was analyzed as a complementary source.

The recovered data was compared against the existing PostgreSQL records using match IDs to identify the missing matches.

A team-name mapping was required because different sources use different names for the same team.

For example:

```text
Sarmiento Junin       → Sarmiento
Argentinos Jrs        → Argentinos Jrs.
Central Cordoba       → Central Córdoba
Velez Sarsfield       → Vélez Sarsfield
Huracan               → Huracán
Union de Santa Fe     → Unión Santa Fe
Newells Old Boys      → Newell's
Talleres Cordoba      → Talleres
Lanus                 → Lanús
```

After the missing records were recovered and loaded, the dataset was validated again.

## PostgreSQL Database

The database is:

```text
liga_argentina_clausura2026
```

The database uses three main tables.

### `teams`

Stores the teams participating in the competition.

```text
id
name
```

### `rounds`

Stores the competition rounds.

```text
id
name
```

### `matches`

Stores the matches and their results.

```text
id
date
round_id
home_team_id
away_team_id
home_score
away_score
```

The `matches` table uses foreign keys to connect each match with its corresponding teams and round.

The relational structure allows match data to be used for analytical SQL queries without duplicating team or round information.

## Current Dataset

The current dataset contains:

* 16 rounds
* 15 matches per round
* 30 teams
* 240 matches

The expected number of matches is:

```text
16 rounds × 15 matches = 240 matches
```

The dataset was verified by counting the matches for each round after the historical data recovery.

## Loading Data

`get_teams.py` loads the teams into PostgreSQL.

`get_rounds.py` loads the competition rounds.

`get_matches.py` reads the processed JSON data and loads the matches into PostgreSQL.

The match loading process:

1. Reads `matches.json`.
2. Finds the corresponding team IDs.
3. Finds the corresponding round ID.
4. Inserts the match into PostgreSQL.
5. Uses the match ID to avoid duplicate records.

## Data Analysis

The PostgreSQL database provides the foundation for the next stage of the project: football data analysis using SQL.

Planned analytical queries include:

* League standings
* Points obtained by each team
* Wins, draws and losses
* Goals scored and conceded
* Goal difference
* Home vs. away performance
* Performance by round
* Recent form
* Team performance trends

The analytical results will later be connected to Power BI to build dashboards and visualizations.

## What I Learned

Through this project I have practiced:

* Making HTTP requests with Python
* Parsing semi-structured data
* Working with regular expressions
* Processing JSON data
* Validating datasets
* Handling duplicate records
* Comparing data from different sources
* Normalizing entity names
* Connecting Python to PostgreSQL
* Writing SQL queries
* Working with primary and foreign keys
* Designing a relational database
* Building an ETL-style data pipeline
* Handling real-world data quality issues

## Next Steps

Planned improvements:

* Create analytical SQL queries
* Generate the league standings from match data
* Add football performance metrics
* Connect PostgreSQL to Power BI
* Build interactive dashboards
* Improve incremental loading logic
* Add stronger data quality checks
* Automate the extraction and loading process

## Project Status

**Current status: Data extraction, validation, historical data recovery and PostgreSQL loading completed.**

The next stage is to build the analytical layer using SQL and connect the resulting data to Power BI.
