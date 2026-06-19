import cv2
import numpy as np
from PIL import Image

def remove_glare(image: Image.Image) -> Image.Image:
    """Detects and inpaints glare/highlight areas in the image.
    
    Args:
        image (PIL.Image.Image): Input PIL image.
        
    Returns:
        PIL.Image.Image: Degen-glared PIL image.
    """
    print("[Preprocessing] Applying glare removal filter...")
    # Convert PIL to OpenCV BGR
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Threshold the image to locate glare (bright spots close to 255)
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    
    # Dilate the mask slightly to include edges
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)
    
    # Inpaint the glare regions using Telea algorithm
    inpainted = cv2.inpaint(img, mask, inpaintRadius=5, flags=cv2.INPAINT_TELEA)
    
    # Convert back to RGB and PIL Image
    rgb_img = cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB)
    print("[Preprocessing] Glare removal filter applied.")
    return Image.fromarray(rgb_img)
