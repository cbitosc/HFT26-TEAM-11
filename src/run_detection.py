import os
import json
import numpy as np
from PIL import Image
from PytorchWildlife.models import detection as pw_detection

print("Loading MegaDetector...")

model = pw_detection.MegaDetectorV6(
    version="MDV6-yolov10-c",
    device="cpu"
)

image_folder = "data/images"
os.makedirs("data", exist_ok=True)

results = []
images = sorted(os.listdir(image_folder))
for i, filename in enumerate(images):

    image_path = os.path.join(image_folder, filename)

    image = np.array(
        Image.open(image_path).convert("RGB")
    )

    prediction = model.single_image_detection(
        image,
        img_path=image_path
    )

    detections = prediction["detections"]

    image_results = []

    for j in range(len(detections)):
        image_results.append({
            "bbox": detections.xyxy[j].tolist(),
            "confidence": float(detections.confidence[j]),
            "class_id": int(detections.class_id[j])
        })

    results.append({
        "image": filename,
        "detections": image_results
    })

    if (i + 1) % 100 == 0:
        print(f"Processed {i + 1}/{len(images)}")
with open("data/detections.json", "w") as f:
    json.dump(results, f, indent=4)

print("\nDetection complete!")
print("Results saved to data/detections_test.json")