from datetime import datetime, timedelta
from src.pipeline.burst_merge import merge_bursts

def frame(t, species="coyote", cam="c1", conf=0.9):
    return {"camera_id": cam, "taken_at": datetime(2026, 1, 1) + timedelta(seconds=t),
            "species": species, "confidence": conf, "image_id": f"img{t}"}

def test_close_frames_merge():
    assert len(merge_bursts([frame(0), frame(10), frame(20)])) == 1

def test_far_frames_split():
    assert len(merge_bursts([frame(0), frame(500)])) == 2

def test_different_cameras_split():
    assert len(merge_bursts([frame(0), frame(5, cam="c2")])) == 2
