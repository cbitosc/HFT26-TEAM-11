import os
import json
from PIL import Image

image_folder = "data/images"
crop_folder = "data/crops"

os.makedirs(crop_folder, exist_ok=True)

with open("data/detections.json", "r") as f:
    results = json.load(f)

print("Images in detection file:", len(results))

count = 0

for item in results:
    image_path = os.path.join(image_folder, item["image"])

    if not os.path.exists(image_path):
        continue

    image = Image.open(image_path).convert("RGB")

    for i, detection in enumerate(item["detections"]):

        if detection["class_id"] != 0:
            continue

        x1, y1, x2, y2 = map(int, detection["bbox"])

        # Keep coordinates within image boundaries
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(image.width, x2)
        y2 = min(image.height, y2)

        if x2 <= x1 or y2 <= y1:
            continue

        crop = image.crop((x1, y1, x2, y2))

        filename = f"animal_{count}.jpg"
        crop.save(os.path.join(crop_folder, filename))
        count += 1

print("Animal crops extracted:", count)