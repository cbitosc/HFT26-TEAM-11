import csv
import os
from PIL import Image

valid = 0
corrupted = 0

with open("data/subset.csv", newline="") as f:
    rows = list(csv.DictReader(f))

for row in rows:
    path = os.path.join("data/images", row["file_name"])

    try:
        with Image.open(path) as img:
            img.verify()
        valid += 1
    except Exception:
        corrupted += 1

print("Total images:", len(rows))
print("Valid images:", valid)
print("Corrupted/missing:", corrupted)