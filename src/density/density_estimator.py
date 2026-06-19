import os
import random
import numpy as np
from PIL import Image
from src.density.csrnet import CSRNet

class DensityEstimator:
    def __init__(self, weights_path: str = "models/weights/csrnet.pt"):
        """Initializes the CSRNet density estimator.
        
        If weights are not found, falls back to Mock Density estimation.
        """
        self.weights_path = weights_path
        self.model = None
        self.mock_mode = True
        
        print(f"[DensityEstimator] Checking for weights at {self.weights_path}...")
        if os.path.exists(self.weights_path):
            try:
                import torch
                self.model = CSRNet(load_weights=False)
                # Load weights onto CPU by default
                self.model.load_state_dict(torch.load(self.weights_path, map_location=torch.device('cpu')))
                self.model.eval()
                self.mock_mode = False
                print("[DensityEstimator] CSRNet weights loaded successfully.")
            except Exception as e:
                print(f"[DensityEstimator] Error loading CSRNet model: {str(e)}. Using mock estimator.")
        else:
            print("[DensityEstimator] Weights not found. Running in mock/simulation mode.")

    def estimate_density(self, image: Image.Image, particle_count: int = 5) -> tuple[np.ndarray, float]:
        """Generates a density map and calculates the estimated particles per liter.
        
        Args:
            image (PIL.Image.Image): Input image.
            particle_count (int): Particle count (used to place blobs in mock mode).
            
        Returns:
            tuple[np.ndarray, float]: 
                - 2D numpy array (density map)
                - float (estimated particles per liter)
        """
        print(f"[DensityEstimator] Estimating density. Mock Mode: {self.mock_mode}")
        if self.mock_mode or self.model is None:
            return self._run_mock_estimation(image, particle_count)
        else:
            return self._run_real_estimation(image)

    def _run_real_estimation(self, image: Image.Image) -> tuple[np.ndarray, float]:
        """Runs CSRNet inference on the image."""
        try:
            import torch
            import torchvision.transforms as transforms
            
            # Preprocess image for CSRNet: resize to 640x640, convert to tensor, normalize
            transform = transforms.Compose([
                transforms.Resize((640, 640)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            
            # Ensure RGB
            if image.mode != "RGB":
                image = image.convert("RGB")
                
            img_tensor = transform(image).unsqueeze(0) # [1, 3, 640, 640]
            
            with torch.no_grad():
                density_map = self.model(img_tensor).squeeze(0).squeeze(0).numpy() # [80, 80] or similar depending on pooling
                
            # Density map sum equals the estimated count
            estimated_count = float(np.sum(density_map))
            # Density per liter is scaled based on standard sample volume (e.g. 0.5 Liters)
            density_per_liter = estimated_count * 2.0
            
            # Clip negative values in density map
            density_map = np.clip(density_map, 0, None)
            
            return density_map, density_per_liter
            
        except Exception as e:
            print(f"[DensityEstimator] Real estimation failed: {str(e)}. Falling back to mock.")
            return self._run_mock_estimation(image, 5)

    def _run_mock_estimation(self, image: Image.Image, particle_count: int) -> tuple[np.ndarray, float]:
        """Generates a synthetic density map with gaussian blobs for visualization."""
        # Output size 80x80 (standard VGG output resolution is 1/8 of input size 640x640)
        h, w = 80, 80
        density_map = np.zeros((h, w), dtype=np.float32)
        
        # Place a gaussian blob for each particle
        num_blobs = max(3, particle_count)
        for _ in range(num_blobs):
            # Center of the blob
            cx = random.randint(10, w - 10)
            cy = random.randint(10, h - 10)
            sigma = random.uniform(2.0, 5.0)
            
            # Draw gaussian
            x = np.arange(0, w, 1, float)
            y = np.arange(0, h, 1, float)[:, np.newaxis]
            
            # Gaussian formula
            g = np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2.0 * sigma ** 2))
            # Scale so sum is approximately 1.0 (representing one particle)
            g_sum = np.sum(g)
            if g_sum > 0:
                density_map += (g / g_sum)
                
        # Calculate particles per liter (mock: random between 5 and 150)
        density_per_liter = float(num_blobs * 12.5 + random.uniform(1.0, 5.0))
        
        return density_map, density_per_liter
