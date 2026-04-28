import torch
import clip
from PIL import Image
from .models import model_clip, preprocess, device, clip, labels, risk_labels

"""
tukaj so funkcije ai komponente, ki dejasno delajo nekej s slikami
lahko za to naredimo tudi posebej modul, če bodo stvari kompleksne
"""

def classify_image_with_clip(image: Image.Image) -> dict:
    
    image_input = preprocess(image).unsqueeze(0).to(device)
    text_input = clip.tokenize(labels).to(device)

    with torch.no_grad():
        logits_per_image, _ = model_clip(image_input, text_input)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()[0]

    results = [
        {
            "label": label,
            "score": float(prob)
        }
        for label, prob in zip(labels, probs)
    ]

    risky_results = [
        r for r in results
        if r["label"] in risk_labels and r["score"] >= 0.3
    ]

    if risky_results:
        return {
            "decision": "needs_review",
            "risk_level": "medium",
            "reasons": risky_results,
            "all_scores": results
        }

    return {
        "decision": "approved",
        "risk_level": "low",
        "reasons": [],
        "all_scores": results
    }