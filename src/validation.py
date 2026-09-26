import json
from datetime import date, datetime
from collections import Counter


# Load data

with open("matches.json", "r", encoding="utf-8") as file:
    matches = json.load(file)

print("Matches loaded:", len(matches))


# Validate IDs

ids = [
    match["id"]
    for match in matches
]

unique_ids = set(ids)

print("\n--- IDs ---")
print("Total IDs:", len(ids))
print("Unique IDs:", len(unique_ids))
print("Duplicate IDs:", len(ids) - len(unique_ids))


# Validate required fields

fields = [
    "id",
    "date",
    "round",
    "home",
    "away"
]

print("\n--- Missing fields ---")

for field in fields:

    missing = sum(
        1
        for match in matches
        if not match.get(field)
    )

    print(
        field + ":",
        missing
    )


# Check match results

with_result = 0
without_result = 0

for match in matches:

    if (
        match.get("home_score") is not None
        and match.get("away_score") is not None
    ):
        with_result += 1
    else:
        without_result += 1


print("\n--- Results ---")
print("With result:", with_result)
print("Without result:", without_result)


# Check matches without results

today = date.today()

past_without_result = []
future_without_result = []

for match in matches:

    if (
        match.get("home_score") is None
        or match.get("away_score") is None
    ):

        match_date = datetime.fromisoformat(
            match["date"]
        ).date()

        if match_date < today:
            past_without_result.append(match)
        else:
            future_without_result.append(match)


print("\n--- Date validation ---")

print(
    "Without result and past date:",
    len(past_without_result)
)

print(
    "Without result and future date:",
    len(future_without_result)
)


# Show suspicious matches

if past_without_result:

    print("\n⚠️ Matches without a result and past date:")

    for match in past_without_result:

        print(
            match["date"],
            "|",
            match["round"],
            "|",
            match["home"],
            "vs",
            match["away"]
        )

else:

    print(
        "\n✅ No matches without a result "
        "with a past date."
    )


# Count matches by round

round_counts = Counter(
    match["round"]
    for match in matches
)

print("\n--- Matches by round ---")

for round_name, count in sorted(
    round_counts.items(),
    key=lambda x: int(x[0].split()[-1])
):

    print(
        round_name,
        ":",
        count
    )
    
