from PIL import Image
from .image_classifier import classify_image_with_clip

# moderacija sprejete slike
def moderate_image(image: Image.Image) -> dict:

    """
    tukej lahko recimo kliče več funkcij iz ai.py / izvede tist pipeline
    
    recimo:
    YOLO prepozna predmete na sliki
    naredi seznam teh prdmetov
    vsakega od teh da CLIPu
    če je pri kateremkoli od teh predmetov problem, pol ni ok
    

    result = classify_image(image_bytes, filename)

    return result"""

    clip_result = classify_image_with_clip(image)

    return {
        "decision": clip_result["decision"],
        "reasons": clip_result["reasons"],
        # to show probability of all labels
        #"full_clip_result": clip_result
    }
