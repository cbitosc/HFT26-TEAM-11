import json
import csv
from pathlib import Path
from datetime import datetime
from PIL import Image

from pipeline.burst_merge import merge_bursts
from pipeline.config import UNIDENTIFIED

# Paths
OUTPUT_DIR = Path("src/dashboard/public/representative_images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load metadata
with open("data/subset.csv", "r") as f:
    metadata = list(csv.DictReader(f))

metadata_map = {row["file_name"]: row for row in metadata}

# Load predictions
with open("data/predictions.json", "r") as f:
    predictions = json.load(f)

frames = []

for prediction in predictions:
    filename = prediction["image"]
    row = metadata_map.get(filename)

    if row is None:
        continue

    image_path = Path("data/images") / filename

    if not image_path.exists():
        continue

    species = prediction["species"]

    if species == "unknown":
        species = UNIDENTIFIED

    timestamp = datetime.strptime(
        row["timestamp"], "%Y-%m-%d %H:%M:%S"
    )

    with Image.open(image_path) as img:
        width, height = img.size

    x1, y1, x2, y2 = prediction["bbox"]

    x1 = max(0, min(x1, width))
    y1 = max(0, min(y1, height))
    x2 = max(0, min(x2, width))
    y2 = max(0, min(y2, height))

    if x2 <= x1 or y2 <= y1:
        continue

    normalized_box = [
        round(x1 / width, 6),
        round(y1 / height, 6),
        round((x2 - x1) / width, 6),
        round((y2 - y1) / height, 6)
    ]

    frames.append({
        "camera_id": row["location"],
        "taken_at": timestamp,
        "species": species,
        "confidence": prediction["species_confidence"],
        "image_id": filename,
        "rep_box": normalized_box,
        "image_path": str(image_path)
    })

# Merge detections into sightings
sightings = merge_bursts(frames)

# Generate representative crops
# Generate representative original images
for sighting in sightings:
    image_path = sighting["rep_source_path"]

    safe_id = sighting["sighting_id"].replace(":", "-")
    image_name = f"{safe_id}.jpg"

    output_dir = Path(
        "wildlife-dashboard/public/camera_images"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / image_name

    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img.save(output_path, "JPEG", quality=95)

    sighting["rep_image"] = "/camera_images/" + image_name

    del sighting["rep_source_path"]

# Save dashboard sightings
output_path = Path("wildlife-dashboard/src/data/sightings.json")
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "w") as f:
    json.dump(sightings, f, indent=2)

print("Dashboard sightings generated!")
print("Total sightings:", len(sightings))
print("Representative images:", len(sightings))
print("Saved to:", output_path)