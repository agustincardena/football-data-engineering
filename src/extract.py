import re
import requests
from datetime import datetime
from collections import Counter
import json


# Download the page

url = "https://ar.soccerway.com/argentina/liga-profesional/"

response = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=10
)

print("Status code:", response.status_code)


# Split matches

events = response.text.split("¬~AA÷")

print("Blocks found:", len(events) - 1)

for block in events[1:]:
    round_match = re.search(r"¬ER÷(.*?)¬", block)

    if round_match and round_match.group(1) in ["Jornada 1", "Jornada 2"]:
        print(
            round_match.group(1),
            "|",
            block[:300]
        )


# Extract match data

matches = []

for block in events[1:]:

    # Match ID
    match_id = block.split("¬", 1)[0]

    # Teams
    home = re.search(r"¬CX÷(.*?)¬", block)
    away = re.search(r"¬AF÷(.*?)¬", block)

    # Round
    round_ = re.search(r"¬ER÷(.*?)¬", block)

    # Result
    home_score = re.search(r"¬AG÷(.*?)¬", block)
    away_score = re.search(r"¬AH÷(.*?)¬", block)

    # Date
    timestamp = re.search(r"¬AD÷(.*?)¬", block)

    # Skip blocks without a timestamp
    if not timestamp:
        continue

    date = datetime.fromtimestamp(
        int(timestamp.group(1))
    )

    matches.append({
        "id": match_id,
        "date": date,
        "round": round_.group(1) if round_ else None,
        "home": home.group(1) if home else None,
        "away": away.group(1) if away else None,
        "home_score": home_score.group(1) if home_score else None,
        "away_score": away_score.group(1) if away_score else None
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

with open("matches.json", "w", encoding="utf-8") as file:
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

print("Data saved to matches.json")


# Show results

print("Matches extracted:", len(matches))

print("\nFirst matches:")

for match in matches[:10]:

    print(
        match["date"],
        "|",
        match["round"],
        "|",
        match["home"],
        "vs",
        match["away"],
        "|",
        match["home_score"],
        "-",
        match["away_score"]
    )


print("\nLast matches:")

for match in matches[-10:]:

    print(
        match["date"],
        "|",
        match["round"],
        "|",
        match["home"],
        "vs",
        match["away"],
        "|",
        match["home_score"],
        "-",
        match["away_score"]
    )


# Count matches by round

round_counts = Counter(
    match["round"]
    for match in matches
)

print("\nMatches by round:")

for round_name, count in sorted(round_counts.items()):

    print(
        round_name,
        ":",
        count
    )