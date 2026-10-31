import json
import csv
import random
from collections import defaultdict

random.seed(42)

# Load annotations
with open("data/annotations/image-level-annotations.json") as f:
    data = json.load(f)

# Load official camera splits
with open("data/annotations/CaltechCameraTrapsSplits_v0.json") as f:
    splits = json.load(f)["splits"]

train_locations = set(splits["train"])
val_locations = set(splits["val"])

categories = {
    c["id"]: c["name"] for c in data["categories"]
}

images = {
    img["id"]: img for img in data["images"]
}

# Store ALL labels belonging to each image
image_labels = defaultdict(set)

for ann in data["annotations"]:
    image_labels[ann["image_id"]].add(
        categories[ann["category_id"]]
    )

train_images = []
val_images = []

for image_id, image in images.items():

    labels = image_labels.get(image_id, {"unknown"})
    location = image["location"]

    row = {
        "image_id": image_id,
        "file_name": image["file_name"],
        "location": location,
        "timestamp": image["date_captured"],
        "labels": "|".join(sorted(labels))
    }

    if location in train_locations:
        train_images.append(row)

    elif location in val_locations:
        val_images.append(row)

# Select images
train_selected = random.sample(train_images, 4000)
val_selected = random.sample(val_images, 1000)

# Save CSV
with open("data/subset.csv", "w", newline="") as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "image_id",
            "file_name",
            "location",
            "timestamp",
            "labels",
            "split"
        ]
    )

    writer.writeheader()

    for row in train_selected:
        row["split"] = "train"
        writer.writerow(row)

    for row in val_selected:
        row["split"] = "val"
        writer.writerow(row)

print("Corrected dataset selection!")
print("Training:", len(train_selected))
print("Validation:", len(val_selected))
print("Total:", len(train_selected) + len(val_selected))
print("Saved: data/subset.csv")