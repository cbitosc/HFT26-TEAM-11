import os
import json
import csv
from PIL import Image
from collections import Counter

IMAGE_DIR = "data/images"
CROP_DIR = "data/crops_labelled"

os.makedirs(CROP_DIR, exist_ok=True)

# Classes with sufficient examples
allowed_species = {
    "opossum", "coyote", "deer", "raccoon",
    "rabbit", "cat", "bobcat", "bird",
    "dog", "squirrel", "rodent", "skunk", "fox"
}

# Load selected images
with open("data/subset.csv", "r") as f:
    subset = list(csv.DictReader(f))

selected_files = {row["file_name"] for row in subset}

# Load annotations
with open("data/annotations/bounding-box-annotations.json", "r") as f:
    data = json.load(f)

image_map = {
    img["id"]: img["file_name"]
    for img in data["images"]
}

category_map = {
    cat["id"]: cat["name"]
    for cat in data["categories"]
}

counts = Counter()
crop_number = 0

for ann in data["annotations"]:

    filename = image_map.get(ann["image_id"])
    species = category_map.get(ann["category_id"])

    if filename not in selected_files:
        continue

    if species not in allowed_species:
        continue

    image_path = os.path.join(IMAGE_DIR, filename)

    if not os.path.exists(image_path):
        continue

    image = Image.open(image_path).convert("RGB")

    x, y, w, h = ann["bbox"]

    x1 = max(0, int(x))
    y1 = max(0, int(y))
    x2 = min(image.width, int(x + w))
    y2 = min(image.height, int(y + h))

    if x2 <= x1 or y2 <= y1:
        continue

    crop = image.crop((x1, y1, x2, y2))

    if crop.width < 10 or crop.height < 10:
        continue

    species_folder = os.path.join(CROP_DIR, species)
    os.makedirs(species_folder, exist_ok=True)

    crop.save(os.path.join(species_folder, f"{crop_number}.jpg"))

    counts[species] += 1
    crop_number += 1

print("\nLabelled crop extraction complete!")
print("Total crops:", crop_number)

for species, count in counts.most_common():
    print(f"{species}: {count}")