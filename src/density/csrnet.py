import torch
import torch.nn as nn
from torchvision import models

class CSRNet(nn.Module):
    def __init__(self, load_weights: bool = False):
        """CSRNet Model Architecture for density map estimation.
        
        Dilated Convolutional Neural Network with VGG-16 backbone features.
        
        Args:
            load_weights (bool): If True, attempts to load pre-trained VGG-16 features.
        """
        super(CSRNet, self).__init__()
        self.seen = 0
        
        # Front-end features (first 10 layers of VGG-16)
        self.frontend_feat = [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512]
        self.backend_feat = [512, 512, 512, 256, 128, 64]
        
        self.frontend = make_layers(self.frontend_feat)
        self.backend = make_layers(self.backend_feat, in_channels=512, dilated=True)
        self.output_layer = nn.Conv2d(64, 1, kernel_size=1)
        
        # Initialize weights
        self._initialize_weights()
        
        if load_weights:
            try:
                print("[CSRNet] Downloading/loading pre-trained VGG-16 weights for front-end...")
                # Try loading VGG-16 weights (older torchvision version uses pretrained=True, newer uses weights=VGG16_Weights.DEFAULT)
                try:
                    from torchvision.models import VGG16_Weights
                    vgg16 = models.vgg16(weights=VGG16_Weights.DEFAULT)
                except ImportError:
                    vgg16 = models.vgg16(pretrained=True)
                
                # Copy frontend weights
                vgg_features = list(vgg16.features.children())
                frontend_features = list(self.frontend.children())
                
                # Map conv layers from VGG16 (which has maxpools too)
                vgg_idx = 0
                for f_layer in frontend_features:
                    if isinstance(f_layer, nn.Conv2d):
                        # Find next conv in VGG
                        while vgg_idx < len(vgg_features) and not isinstance(vgg_features[vgg_idx], nn.Conv2d):
                            vgg_idx += 1
                        if vgg_idx < len(vgg_features):
                            f_layer.weight.data.copy_(vgg_features[vgg_idx].weight.data)
                            f_layer.bias.data.copy_(vgg_features[vgg_idx].bias.data)
                            vgg_idx += 1
                print("[CSRNet] Frontend weights loaded successfully.")
            except Exception as e:
                print(f"[CSRNet] Could not load VGG-16 weights: {str(e)}. Using random initialization.")

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.frontend(x)
        x = self.backend(x)
        x = self.output_layer(x)
        return x

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.normal_(m.weight, std=0.01)
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

def make_layers(cfg: list, in_channels: int = 3, batch_norm: bool = False, dilated: bool = False) -> nn.Sequential:
    """Helper function to compile layer lists into a sequential module."""
    if dilated:
        d_rate = 2
    else:
        d_rate = 1
        
    layers = []
    for v in cfg:
        if v == 'M':
            layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
        else:
            conv2d = nn.Conv2d(in_channels, v, kernel_size=3, padding=d_rate, dilation=d_rate)
            if batch_norm:
                layers += [conv2d, nn.BatchNorm2d(v), nn.ReLU(inplace=True)]
            else:
                layers += [conv2d, nn.ReLU(inplace=True)]
            in_channels = v
    return nn.Sequential(*layers)
