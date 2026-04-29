from PIL import Image
from .image_classifier import classify_image_with_clip

# moderacija sprejete slike
def moderate_image(image: Image.Image) -> dict:

    clip_result = classify_image_with_clip(image)

    return {
        "decision": clip_result["decision"],
        "reasons": clip_result["reasons"],
        # to show probability of all labels
        #"full_clip_result": clip_result
    }
