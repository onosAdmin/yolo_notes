import os
from groundingdino.util.inference import load_model, load_image, predict, annotate
import cv2

# Use absolute paths to avoid any confusion
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "groundingdino/config/GroundingDINO_SwinT_OGC.py")
WEIGHTS_PATH = os.path.join(SCRIPT_DIR, "weights/groundingdino_swint_ogc.pth")
IMAGE_PATH = "/media/data/progetti/prog_miei/computer_vision/yolo_video/riconoscimento_lego/dataset_source/made_myself/2x2_brick/2025-05-03-133029_1.jpg"

# Verify that the files exist
print(f"Checking if config exists: {os.path.exists(CONFIG_PATH)}")
print(f"Checking if weights exist: {os.path.exists(WEIGHTS_PATH)}")
print(f"Checking if image exists: {os.path.exists(IMAGE_PATH)}")


try:
    # Try to load the file as a PyTorch model
    torch.load(file_path, map_location="cpu")
    print("PyTorch model ok")
except Exception:
    print("PyTorch model ERROR")







# Text prompt and thresholds
TEXT_PROMPT = "lego . person . dog ."
BOX_TRESHOLD = 0.35
TEXT_TRESHOLD = 0.25

try:
    # Load the model
    print("Loading model...")
    model = load_model(CONFIG_PATH, WEIGHTS_PATH)
    
    # Load and process the image
    print("Loading image...")
    image_source, image = load_image(IMAGE_PATH)
    
    print("Running inference...")
    boxes, logits, phrases = predict(
        model=model,
        image=image,
        caption=TEXT_PROMPT,
        box_threshold=BOX_TRESHOLD,
        text_threshold=TEXT_TRESHOLD
    )
    
    print(f"Detected {len(boxes)} objects: {phrases}")
    
    # Annotate and save
    annotated_frame = annotate(image_source=image_source, boxes=boxes, logits=logits, phrases=phrases)
    output_path = os.path.join(SCRIPT_DIR, "annotated_image.jpg")
    cv2.imwrite(output_path, annotated_frame)
    print(f"Saved annotated image to {output_path}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()