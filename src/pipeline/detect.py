"""Tier 1: run MegaDetector over a folder, write detections.json (precompute)."""
import json, sys
from pathlib import Path
from .config import DETECTION_THRESHOLD


def run(image_dir: str, out_path: str = "data/detections.json"):
    from PytorchWildlife.models import detection as pw_detection  # imported lazily
    model = pw_detection.MegaDetectorV5(device="cuda", pretrained=True)
    results = []
    for img in sorted(Path(image_dir).glob("*.jpg")):
        r = model.single_image_detection(str(img), det_conf_thres=DETECTION_THRESHOLD)
        dets = r["detections"]
        results.append({
            "image_id": img.stem,
            "is_empty": len(dets) == 0,
            "boxes": dets.xyxy.tolist(),
            "conf": dets.confidence.tolist(),
            "category": dets.class_id.tolist(),  # 0 animal, 1 person, 2 vehicle
        })
    Path(out_path).write_text(json.dumps(results))
    print(f"{len(results)} images, {sum(x['is_empty'] for x in results)} empty")


if __name__ == "__main__":
    run(sys.argv[1])
