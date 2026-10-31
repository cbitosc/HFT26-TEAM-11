import json
import os

base_path = "data/annotations"

files = [
    "image-level-annotations.json",
    "bounding-box-annotations.json",
    "CaltechCameraTrapsSplits_v0.json"
]

for filename in files:
    path = os.path.join(base_path, filename)

    print("\n" + "=" * 50)
    print("FILE:", filename)

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("Main keys:", list(data.keys()))

    for key, value in data.items():
        if isinstance(value, list):
            print(f"{key}: {len(value)} records")

            if value:
                print("Sample:", value[0])

        elif isinstance(value, dict):
            print(f"{key}: dictionary")
            print("Subkeys:", list(value.keys()))

    if filename == files[2]:
        for split, locations in data["splits"].items():
            print(
                split,
                "unique locations:",
                len(set(locations))
            )
            # Display all animal categories

path = "data/annotations/image-level-annotations.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("\nAVAILABLE ANIMAL CATEGORIES")

for category in data["categories"]:
    print(category["id"], ":", category["name"])