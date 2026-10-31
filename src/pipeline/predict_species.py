import os
import json
import torch
import torch.nn as nn
import numpy as np

from PIL import Image
from torchvision import models, transforms
from PytorchWildlife.models import detection as pw_detection

# Paths
IMAGE_DIR = "data/images"
MODEL_PATH = "models/wildlife_classifier.pth"
DETECTION_PATH = "data/detections.json"
OUTPUT_PATH = "data/predictions.json"

device = torch.device("cpu")

# Load species classifier
print("Loading species classifier...")

checkpoint = torch.load(
    MODEL_PATH,
    map_location=device,
    weights_only=False
)

class_names = checkpoint["class_names"]

classifier = models.mobilenet_v3_small(weights=None)
input_features = classifier.classifier[3].in_features

classifier.classifier[3] = nn.Linear(
    input_features, len(class_names)
)

classifier.load_state_dict(checkpoint["model_state_dict"])
classifier.eval()

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

# Load MegaDetector results
with open(DETECTION_PATH, "r") as f:
    detections = json.load(f)

print("Images to process:", len(detections))

results = []

# Classify detected animals
for index, item in enumerate(detections):

    image_path = os.path.join(IMAGE_DIR, item["image"])

    if not os.path.exists(image_path):
        continue

    image = Image.open(image_path).convert("RGB")

    for detection in item["detections"]:

        # Only process animal detections
        if detection["class_id"] != 0:
            continue

        x1, y1, x2, y2 = map(int, detection["bbox"])

        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(image.width, x2)
        y2 = min(image.height, y2)

        if x2 <= x1 or y2 <= y1:
            continue

        crop = image.crop((x1, y1, x2, y2))

        input_tensor = transform(crop).unsqueeze(0)

        with torch.no_grad():
            output = classifier(input_tensor)
            probabilities = torch.softmax(output, dim=1)
            confidence, prediction = torch.max(probabilities, dim=1)

        score = float(confidence.item())

        # Low-confidence predictions remain unknown
        if score < 0.60:
            species = "unknown"
        else:
            species = class_names[prediction.item()]

        results.append({
            "image": item["image"],
            "bbox": detection["bbox"],
            "detector_confidence": detection["confidence"],
            "species": species,
            "species_confidence": round(score, 4)
        })

    if (index + 1) % 500 == 0:
        print(f"Processed {index + 1}/{len(detections)} images")

# Save predictions
with open(OUTPUT_PATH, "w") as f:
    json.dump(results, f, indent=2)

print("\nSpecies prediction complete!")
print("Total animal predictions:", len(results))
print("Saved to:", OUTPUT_PATH)