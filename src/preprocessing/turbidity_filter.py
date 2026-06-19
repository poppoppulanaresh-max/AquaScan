import cv2
import numpy as np
from PIL import Image

def correct_turbidity(image: Image.Image) -> Image.Image:
    """Corrects low contrast and color cast caused by water turbidity (murkiness).
    
    Applies Gray World white-balancing to remove color casts and uses details-enhancement
    filtering to sharpen micro-particles in water.
    
    Args:
        image (PIL.Image.Image): Input PIL image.
        
    Returns:
        PIL.Image.Image: Enhanced PIL image.
    """
    print("[Preprocessing] Applying turbidity correction filter...")
    # Convert PIL to OpenCV BGR
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # 1. Gray World White Balance
    # Compute mean color channel values
    mean_b = np.mean(img[:, :, 0])
    mean_g = np.mean(img[:, :, 1])
    mean_r = np.mean(img[:, :, 2])
    
    # Target mean is the average of all three channel averages
    mean_gray = (mean_b + mean_g + mean_r) / 3.0
    
    # Scale channels
    scale_b = mean_gray / (mean_b + 1e-6)
    scale_g = mean_gray / (mean_g + 1e-6)
    scale_r = mean_gray / (mean_r + 1e-6)
    
    img[:, :, 0] = np.clip(img[:, :, 0] * scale_b, 0, 255)
    img[:, :, 1] = np.clip(img[:, :, 1] * scale_g, 0, 255)
    img[:, :, 2] = np.clip(img[:, :, 2] * scale_r, 0, 255)
    
    # 2. Detail enhancement to highlight submerged particles
    # Using unsharp masking
    gaussian_blur = cv2.GaussianBlur(img, (5, 5), 1.5)
    sharpened = cv2.addWeighted(img, 1.5, gaussian_blur, -0.5, 0)
    
    # Convert back to RGB and PIL Image
    rgb_img = cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB)
    print("[Preprocessing] Turbidity correction completed.")
    return Image.fromarray(rgb_img)
