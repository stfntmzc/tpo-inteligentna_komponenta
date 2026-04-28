from pathlib import Path

import torch
import clip

BASE_DIR = Path(__file__).resolve().parent

# loads labels from file in path
def load_labels(path):
    with open(path, "r", encoding="utf-8") as f:
        labels = [
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]
    return labels


device = "cuda" if torch.cuda.is_available() else "cpu"
model_clip, preprocess = clip.load("ViT-B/32", device=device)

labels = load_labels(BASE_DIR / "labels.txt")
risk_labels = load_labels(BASE_DIR / "risk_labels.txt")