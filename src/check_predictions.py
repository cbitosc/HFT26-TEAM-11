import json
from collections import Counter

with open("data/predictions.json", "r") as f:
    predictions = json.load(f)

species_counts = Counter(
    item["species"] for item in predictions
)

print("Total predictions:", len(predictions))
print("\nSpecies distribution:")

for species, count in species_counts.most_common():
    print(f"{species}: {count}")

print("\nUnknown predictions:", species_counts["unknown"])
