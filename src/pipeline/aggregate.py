import json
import csv
from collections import Counter, defaultdict
from datetime import datetime

# Load dashboard sightings
with open("src/dashboard/data/sightings.json", "r") as f:
    sightings = json.load(f)

# Load dataset metadata
with open("data/subset.csv", "r") as f:
    metadata = list(csv.DictReader(f))

# Load predictions
with open("data/predictions.json", "r") as f:
    predictions = json.load(f)

species_counts = Counter()
location_counts = Counter()
hourly_counts = defaultdict(lambda: [0] * 24)

for s in sightings:
    species = s["species"]

    species_counts[species] += 1
    location_counts[s["camera_id"]] += 1

    hour = datetime.fromisoformat(s["start_time"]).hour
    hourly_counts[species][hour] += 1

# Calculate empty image percentage
detected_images = set(p["image"] for p in predictions)
total_images = len(metadata)
empty_images = total_images - len(detected_images)

pct_empty = round(empty_images / total_images * 100, 2)

# Calculate unidentified percentage
unidentified = species_counts["unidentified"]

pct_unidentified = round(
    unidentified / len(sightings) * 100, 2
) if sightings else 0

# Average confidence
mean_confidence = round(
    sum(s["confidence"] for s in sightings) / len(sightings), 4
) if sightings else 0

aggregates = {
    "species_counts": dict(species_counts.most_common()),
    "hourly_counts": dict(hourly_counts),
    "location_counts": dict(location_counts.most_common()),
    "pct_empty": pct_empty,
    "pct_unidentified": pct_unidentified,
    "mean_confidence": mean_confidence,
    "per_class_accuracy": {},
    "clock_flagged_cameras": []
}

# Save dashboard aggregates
with open("src/dashboard/data/aggregates.json", "w") as f:
    json.dump(aggregates, f, indent=2)

print("Analytics generated successfully!")
print("Total sightings:", len(sightings))
print("Empty images:", pct_empty, "%")
print("Unidentified:", pct_unidentified, "%")
print("Mean confidence:", mean_confidence)
print("Saved to src/dashboard/data/aggregates.json")