import cv2
import numpy as np
from PIL import Image

def validate_image(image: Image.Image) -> tuple[bool, str]:
    """Validates the uploaded image for dimensions and color profiles.
    
    Args:
        image (PIL.Image.Image): The uploaded image.
        
    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    print("[Preprocessing] Validating image...")
    if image is None:
        return False, "No image file provided."
        
    try:
        # Check if file is corrupted by verifying its format/size
        width, height = image.size
    except Exception as e:
        return False, f"Image file is corrupted or unreadable: {str(e)}"

    # Check minimum dimensions (relaxed to 100x100px to support wide/small crops)
    if width < 100 or height < 100:
        return False, f"Image size is too small ({width}x{height}px). Minimum required is 100x100px."
        
    # Check channels/color mode
    if image.mode not in ("RGB", "RGBA"):
        # Convert grayscale or other modes to RGB
        try:
            image = image.convert("RGB")
        except Exception:
            return False, f"Unsupported image color profile: {image.mode}."
            
    return True, ""

def preprocess(image: Image.Image) -> Image.Image:
    """Preprocesses the image for model inference.
    
    Resizes to 640x640 maintaining aspect ratio with black padding, applies
    CLAHE contrast enhancement, and performs denoising.
    
    Args:
        image (PIL.Image.Image): Original input image.
        
    Returns:
        PIL.Image.Image: Preprocessed RGB image.
    """
    print("[Preprocessing] Commencing preprocessing pipeline...")
    
    # 1. Convert to RGB if in RGBA
    if image.mode == "RGBA":
        print("[Preprocessing] Converting RGBA image to RGB...")
        image = image.convert("RGB")
        
    # Convert PIL Image to OpenCV NumPy Array (BGR)
    open_cv_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    h, w = open_cv_img.shape[:2]
    
    # 2. Resize maintaining aspect ratio and pad with black to 640x640
    target_size = 640
    scale = target_size / max(h, w)
    new_h, new_w = int(h * scale), int(w * scale)
    
    print(f"[Preprocessing] Resizing image from {w}x{h} to {new_w}x{new_h}...")
    resized_img = cv2.resize(open_cv_img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
    
    # Pad to 640x640
    pad_h = target_size - new_h
    pad_w = target_size - new_w
    top = pad_h // 2
    bottom = pad_h - top
    left = pad_w // 2
    right = pad_w - left
    
    padded_img = cv2.copyMakeBorder(
        resized_img, top, bottom, left, right, 
        cv2.BORDER_CONSTANT, value=[0, 0, 0]
    )
    
    # 3. Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    print("[Preprocessing] Applying CLAHE contrast enhancement...")
    lab = cv2.cvtColor(padded_img, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l_channel)
    limg = cv2.merge((cl, a, b))
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    
    # 4. Denoise with OpenCV fastNlMeansDenoisingColored
    print("[Preprocessing] Running fastNlMeansDenoisingColored (denoising)...")
    denoised_img = cv2.fastNlMeansDenoisingColored(
        enhanced_img, None, h=10, hColor=10, templateWindowSize=7, searchWindowSize=21
    )
    
    # 5. Normalize pixel values (optional standard scale 0-255 mapping)
    print("[Preprocessing] Normalizing pixel intensity...")
    norm_img = np.zeros((target_size, target_size), dtype=np.uint8)
    norm_img = cv2.normalize(denoised_img, norm_img, 0, 255, cv2.NORM_MINMAX)
    
    # Convert BGR back to RGB and return PIL Image
    rgb_img = cv2.cvtColor(norm_img, cv2.COLOR_BGR2RGB)
    print("[Preprocessing] Preprocessing pipeline completed successfully.")
    return Image.fromarray(rgb_img)
