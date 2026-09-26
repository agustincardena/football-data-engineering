import json

from database import get_connection


with open("matches.json", "r", encoding="utf-8") as file:
    matches = json.load(file)

rounds = set()

for match in matches:
    rounds.add(match["round"])

print(f"Total rounds: {len(rounds)}")

for round_ in sorted(rounds, key=lambda x: int(x.split()[-1])):
    print(round_)

connection = get_connection()
cursor = connection.cursor()

for round_ in rounds:
    cursor.execute(
        """
        INSERT INTO rounds (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
        """,
        (round_,)
    )

connection.commit()

cursor.close()
connection.close()

print("Rounds loaded successfully")