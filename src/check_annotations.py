import json
import csv
from collections import Counter

# Load selected images
with open("data/subset.csv", "r") as f:
    subset = list(csv.DictReader(f))

selected_files = {row["file_name"] for row in subset}

# Load bounding-box annotations
with open("data/annotations/bounding-box-annotations.json", "r") as f:
    data = json.load(f)

# Map image IDs to filenames
image_map = {
    img["id"]: img["file_name"]
    for img in data["images"]
}

# Map category IDs to names
category_map = {
    cat["id"]: cat["name"]
    for cat in data["categories"]
}

# Count annotations only for selected images
counts = Counter()

for ann in data["annotations"]:
    filename = image_map.get(ann["image_id"])

    if filename in selected_files:
        species = category_map[ann["category_id"]]

        if species not in ["empty", "car"]:
            counts[species] += 1

print("Labelled animal crops in our subset:\n")

for species, count in counts.most_common():
    print(f"{species}: {count}")

print("\nTotal labelled animal boxes:", sum(counts.values()))
print("Animal categories:", len(counts))