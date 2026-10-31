from src.pipeline.classify import apply_threshold
from src.training.train_classifier import split_by_camera

def test_threshold():
    assert apply_threshold("coyote", 0.4)[0] == "unidentified"
    assert apply_threshold("coyote", 0.9)[0] == "coyote"

def test_camera_split_has_no_overlap():
    train, test = split_by_camera([f"c{i}" for i in range(20)])
    assert not (train & test)
