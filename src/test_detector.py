import torch
from PytorchWildlife.models import detection as pw_detection

print("Loading MegaDetector...")

model = pw_detection.MegaDetectorV6(
    version="MDV6-yolov10-c",
    device="cpu"
)

print("MegaDetector loaded successfully!")