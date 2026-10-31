"""Fine-tune a small classifier on animal crops. Split by CAMERA, not randomly.
Run on Colab/Kaggle GPU. Weights are NOT committed (see .gitignore)."""
import random


def split_by_camera(camera_ids, test_frac=0.25, seed=42):
    cams = sorted(set(camera_ids))
    random.Random(seed).shuffle(cams)
    k = max(1, int(len(cams) * test_frac))
    return set(cams[k:]), set(cams[:k])  # train cameras, held-out cameras


def main():
    import timm, torch  # noqa: F401
    # TODO: load crops, build dataloaders with class weights,
    # model = timm.create_model("efficientnet_b0", pretrained=True, num_classes=N)
    # train, save weights to data/classifier.pt, log per-class metrics
    raise NotImplementedError("Dwayitha: implement training loop")


if __name__ == "__main__":
    main()
