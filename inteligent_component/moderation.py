from PIL import Image
from .image_classifier import classify_image_with_clip
from .config import ModerationConfig

# moderacija sprejete slike
def moderate_image(image: Image.Image, config: ModerationConfig) -> dict:

    clip_result = classify_image_with_clip(image, config)

    return {
        "decision": clip_result["decision"],
        "reasons": clip_result["reasons"],
        # to show probability of all labels
        #"full_clip_result": clip_result
    }
