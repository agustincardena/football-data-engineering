import json

from database import get_connection


# Load Flashscore data

with open("flashscore_historical.json", "r", encoding="utf-8") as file:
    flashscore_matches = json.load(file)


flashscore_jornada1 = [
    match
    for match in flashscore_matches
    if match["round"] == "Jornada 1"
]


# Load PostgreSQL data

connection = get_connection()
cursor = connection.cursor()

cursor.execute(
    """
    SELECT id
    FROM matches
    WHERE round_id = 1
    """
)

database_ids = {
    row[0]
    for row in cursor.fetchall()
}

cursor.close()
connection.close()


# Compare IDs

flashscore_ids = {
    match["id"]
    for match in flashscore_jornada1
}

missing_ids = flashscore_ids - database_ids


# Show results

print("Flashscore Jornada 1:", len(flashscore_ids))
print("PostgreSQL Jornada 1:", len(database_ids))
print("Missing from PostgreSQL:", len(missing_ids))

print("\nMissing matches:")

for match in flashscore_jornada1:

    if match["id"] in missing_ids:

        print(
            match["id"],
            "|",
            match["home"],
            "vs",
            match["away"],
            "|",
            match["home_score"],
            "-",
            match["away_score"]
        )