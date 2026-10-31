"""Merge frames into sightings using sequence id, else timestamp proximity."""

from collections import defaultdict
from .config import BURST_GAP_SECONDS


def merge_bursts(frames, gap_seconds=BURST_GAP_SECONDS):
    groups = defaultdict(list)

    for f in frames:
        groups[(f["camera_id"], f["species"])].append(f)

    sightings = []

    for (camera, species), items in groups.items():
        items.sort(key=lambda f: f["taken_at"])
        current = [items[0]]

        for f in items[1:]:
            prev = current[-1]

            same_seq = (
                f.get("seq_id")
                and f.get("seq_id") == prev.get("seq_id")
            )

            close = (
                f["taken_at"] - prev["taken_at"]
            ).total_seconds() <= gap_seconds

            if same_seq or (not f.get("seq_id") and close):
                current.append(f)
            else:
                sightings.append(_build(camera, species, current))
                current = [f]

        sightings.append(_build(camera, species, current))

    return sightings


def _build(camera, species, frames):
    best = max(frames, key=lambda f: f["confidence"])

    return {
        "sighting_id": (
            f"{camera}-{frames[0]['taken_at'].isoformat()}-{species}"
        ),
        "camera_id": camera,
        "start_time": frames[0]["taken_at"].isoformat(),
        "end_time": frames[-1]["taken_at"].isoformat(),
        "species": species,
        "confidence": best["confidence"],
        "n_frames": len(frames),
        "rep_image": best.get("image_id"),
        "rep_box": best.get("rep_box"),
        "rep_source_path": best.get("image_path")
    }