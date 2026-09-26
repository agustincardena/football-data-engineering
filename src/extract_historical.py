import json
import re
import requests
from datetime import datetime


url = "https://global.flashscore.ninja/2020/x/feed/tr_1_22_naYhNOaA_185_1_-3_en_1"

response = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.soccerway.com/",
        "x-fsign": "SW9D1eZo"
    },
    timeout=10
)

print("Status code:", response.status_code)
print("Response length:", len(response.text))


# Split matches

events = response.text.split("¬~AA÷")

print("Blocks found:", len(events) - 1)


# Extract Round 1 and Round 2

matches = []

for block in events[1:]:

    match_id = block.split("¬", 1)[0]

    round_match = re.search(
        r"¬ER÷(.*?)¬",
        block
    )

    home = re.search(
        r"¬CX÷(.*?)¬",
        block
    )

    away = re.search(
        r"¬AF÷(.*?)¬",
        block
    )

    timestamp = re.search(
        r"¬AD÷(.*?)¬",
        block
    )

    home_score = re.search(
        r"¬AG÷(.*?)¬",
        block
    )

    away_score = re.search(
        r"¬AH÷(.*?)¬",
        block
    )

    if not round_match or not timestamp:
        continue

    round_name = round_match.group(1)

    if round_name not in ["Round 1", "Round 2"]:
        continue

    if not home or not away:
        continue

    date = datetime.fromtimestamp(
        int(timestamp.group(1))
    )

    round_number = int(
        round_name.split()[-1]
    )

    matches.append({
        "id": match_id,
        "date": date,
        "round": f"Jornada {round_number}",
        "home": home.group(1),
        "away": away.group(1),
        "home_score": (
            home_score.group(1)
            if home_score
            else None
        ),
        "away_score": (
            away_score.group(1)
            if away_score
            else None
        )
    })


# Remove duplicate matches

unique_matches = {}

for match in matches:

    unique_matches[match["id"]] = match

matches = list(unique_matches.values())


# Sort by date

matches.sort(
    key=lambda x: x["date"]
)


# Save JSON

with open(
    "flashscore_historical.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        [
            {
                **match,
                "date": match["date"].isoformat()
            }
            for match in matches
        ],
        file,
        ensure_ascii=False,
        indent=4
    )


print("\nData saved to flashscore_historical.json")


# Show results

print(
    "\nMatches extracted:",
    len(matches)
)


print("\nMatches by round:")

for round_number in [1, 2]:

    round_name = f"Jornada {round_number}"

    round_matches = [
        match
        for match in matches
        if match["round"] == round_name
    ]

    print(
        round_name,
        ":",
        len(round_matches)
    )


# Validate total

expected_matches = 30

print("\nValidation:")

if len(matches) == expected_matches:

    print(
        "OK:",
        expected_matches,
        "matches found."
    )

else:

    print(
        "WARNING:",
        len(matches),
        "matches found.",
        "Expected:",
        expected_matches
    )


# Validate duplicate IDs

ids = [
    match["id"]
    for match in matches
]

unique_ids = set(ids)

print(
    "Duplicate IDs:",
    len(ids) - len(unique_ids)
)