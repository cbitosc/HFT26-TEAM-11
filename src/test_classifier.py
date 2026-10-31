import torch
from torchvision import models, transforms
from PIL import Image
import torch.nn as nn
import os

MODEL_PATH = "models/wildlife_classifier.pth"

device = torch.device("cpu")

checkpoint = torch.load(
    MODEL_PATH,
    map_location=device,
    weights_only=False
)

class_names = checkpoint["class_names"]

model = models.mobilenet_v3_small(weights=None)

input_features = model.classifier[3].in_features
model.classifier[3] = nn.Linear(
    input_features, len(class_names)
)

model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

# Test using one labelled crop
species = class_names[0]
folder = os.path.join("data/crops_labelled", species)

image_name = os.listdir(folder)[0]
image_path = os.path.join(folder, image_name)

image = Image.open(image_path).convert("RGB")
image = transform(image).unsqueeze(0)

with torch.no_grad():
    outputs = model(image)
    probabilities = torch.softmax(outputs, dim=1)
    confidence, prediction = torch.max(probabilities, dim=1)

print("Actual species:", species)
print("Predicted species:", class_names[prediction.item()])
print("Confidence:", round(confidence.item() * 100, 2), "%")