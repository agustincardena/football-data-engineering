
import json

from database import get_connection


with open("matches.json", "r", encoding="utf-8") as file:
    matches = json.load(file)

teams = set()

for match in matches:
    teams.add(match["home"])
    teams.add(match["away"])

print(f"Total teams: {len(teams)}")

for team in sorted(teams):
    print(team)

connection = get_connection()
cursor = connection.cursor()

for team in teams:
    cursor.execute(
        """
        INSERT INTO teams (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
        """,
        (team,)
    )

connection.commit()

cursor.close()
connection.close()

print("Teams loaded successfully")

