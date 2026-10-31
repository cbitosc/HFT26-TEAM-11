import json
from collections import Counter

# Load image-level annotations
with open("data/annotations/image-level-annotations.json", "r") as f:
    data = json.load(f)

# Load official splits
with open("data/annotations/CaltechCameraTrapsSplits_v0.json", "r") as f:
    split_data = json.load(f)

train_locations = set(split_data["splits"]["train"])
val_locations = set(split_data["splits"]["val"])

# Map category IDs to names
categories = {
    item["id"]: item["name"]
    for item in data["categories"]
}

# Map image IDs to image information
images = {
    image["id"]: image
    for image in data["images"]
}

# Count categories in training and validation
train_count = Counter()
val_count = Counter()

for annotation in data["annotations"]:

    image = images.get(annotation["image_id"])

    if image is None:
        continue

    category = categories[annotation["category_id"]]
    location = image["location"]

    if location in train_locations:
        train_count[category] += 1

    elif location in val_locations:
        val_count[category] += 1

print("\nTRAINING CATEGORY COUNTS")

for name, count in train_count.most_common():
    print(name, ":", count)

print("\nVALIDATION CATEGORY COUNTS")

for name, count in val_count.most_common():
    print(name, ":", count)