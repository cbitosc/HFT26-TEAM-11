import os
import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split
from sklearn.metrics import classification_report, accuracy_score
import json

# Settings
DATA_DIR = "data/crops_labelled"
MODEL_DIR = "models"
BATCH_SIZE = 16
EPOCHS = 5
IMAGE_SIZE = 224

os.makedirs(MODEL_DIR, exist_ok=True)

# CPU device
device = torch.device("cpu")
print("Using device:", device)

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# Load dataset
dataset = datasets.ImageFolder(DATA_DIR, transform=transform)

class_names = dataset.classes

print("Species:", class_names)
print("Total images:", len(dataset))

# Split dataset
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size

train_data, val_data = random_split(
    dataset,
    [train_size, val_size],
    generator=torch.Generator().manual_seed(42)
)

train_loader = DataLoader(
    train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=0
)

val_loader = DataLoader(
    val_data, batch_size=BATCH_SIZE, shuffle=False, num_workers=0
)

# Load pretrained MobileNetV3-Small
print("\nLoading MobileNetV3-Small...")

weights = models.MobileNet_V3_Small_Weights.DEFAULT
model = models.mobilenet_v3_small(weights=weights)

# Replace final classification layer
input_features = model.classifier[3].in_features

model.classifier[3] = nn.Linear(
    input_features, len(class_names)
)

model = model.to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training
for epoch in range(EPOCHS):

    model.train()
    total_loss = 0

    for images, labels in train_loader:

        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(
        f"Epoch [{epoch + 1}/{EPOCHS}] "
        f"Loss: {total_loss / len(train_loader):.4f}"
    )

# Validation
model.eval()

actual = []
predicted = []

with torch.no_grad():

    for images, labels in val_loader:

        outputs = model(images)
        predictions = torch.argmax(outputs, dim=1)

        actual.extend(labels.numpy())
        predicted.extend(predictions.numpy())

accuracy = accuracy_score(actual, predicted)

print("\nValidation Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(
    classification_report(
        actual,
        predicted,
        labels=list(range(len(class_names))),
        target_names=class_names,
        zero_division=0
    )
)

# Save model
torch.save({
    "model_state_dict": model.state_dict(),
    "class_names": class_names
}, os.path.join(MODEL_DIR, "wildlife_classifier.pth"))

print("\nModel saved successfully!")