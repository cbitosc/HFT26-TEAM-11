import json
from collections import Counter

with open("data/detections.json", "r") as f:
    results = json.load(f)

classes = Counter()

for item in results:
    for detection in item["detections"]:
        classes[detection["class_id"]] += 1

print("Total images:", len(results))
print("Detection counts:", classes)
print("Animal detections:", classes[0])
print("Human detections:", classes[1])
print("Vehicle detections:", classes[2])