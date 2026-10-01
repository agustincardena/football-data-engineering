import json

from database import get_connection


with open("matches.json", "r", encoding="utf-8") as file:
    matches = json.load(file)

connection = get_connection()
cursor = connection.cursor()

for match in matches:
    home_team = match["home"]

    cursor.execute(
        """
        SELECT id
        FROM teams
        WHERE name = %s
        """,
        (home_team,)
    )

    home_team_id = cursor.fetchone()[0]

    away_team = match["away"]

    cursor.execute(
        """
        SELECT id
        FROM teams
        WHERE name = %s
        """,
        (away_team,)
    )

    away_team_id = cursor.fetchone()[0]

    round_name = match["round"]

    cursor.execute(
        """
        SELECT id
        FROM rounds
        WHERE name = %s
        """,
        (round_name,)
    )

    round_id = cursor.fetchone()[0]

    match_id = match["id"]
    match_date = match["date"]
    home_score = match["home_score"]
    away_score = match["away_score"]

    cursor.execute(
        """
        INSERT INTO matches (
            id,
            date,
            round_id,
            home_team_id,
            away_team_id,
            home_score,
            away_score
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
        date = EXCLUDED.date,
        round_id = EXCLUDED.round_id,
        home_team_id = EXCLUDED.home_team_id,
        away_team_id = EXCLUDED.away_team_id,
        home_score = EXCLUDED.home_score,
        away_score = EXCLUDED.away_score
        """,
        (
            match_id,
            match_date,
            round_id,
            home_team_id,
            away_team_id,
            home_score,
            away_score
        )
    )

connection.commit()

cursor.close()
connection.close()