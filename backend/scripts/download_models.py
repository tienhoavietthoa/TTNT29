import os
import urllib.request
import zipfile
from pathlib import Path
import shutil

class ModelDownloader:
    """Download InsightFace pretrained models"""
    
    # Model URLs (Buffalo_L from InsightFace official release)
    MODELS = {
        'det_10g.onnx': 'https://github.com/deepinsight/insightface/releases/download/v0.7/det_10g.onnx',
        'w600k_r50.onnx': 'https://github.com/deepinsight/insightface/releases/download/v0.7/w600k_r50.onnx',
        '2d106det.onnx': 'https://github.com/deepinsight/insightface/releases/download/v0.7/2d106det.onnx',
        '1k3d68.onnx': 'https://github.com/deepinsight/insightface/releases/download/v0.7/1k3d68.onnx',
        'genderage.onnx': 'https://github.com/deepinsight/insightface/releases/download/v0.7/genderage.onnx',
    }
    
    def __init__(self, model_dir: str = "models"):
        self.model_dir = model_dir
        Path(self.model_dir).mkdir(parents=True, exist_ok=True)
    
    def download_all(self):
        """Download all models"""
        print("Downloading InsightFace models...")
        print("=" * 50)
        
        for model_name, url in self.MODELS.items():
            self.download_model(model_name, url)
        
        print("=" * 50)
        print("✓ All models downloaded successfully!")
    
    def download_model(self, model_name: str, url: str):
        """Download single model"""
        filepath = os.path.join(self.model_dir, model_name)
        
        # Check if already exists
        if os.path.exists(filepath):
            print(f"✓ {model_name} already exists")
            return
        
        try:
            print(f"Downloading {model_name}...")
            
            # Progress hook
            def progress_hook(block_num, block_size, total_size):
                downloaded = block_num * block_size
                if downloaded >= total_size:
                    print(f"  ✓ Downloaded {model_name}")
            
            urllib.request.urlretrieve(url, filepath, progress_hook)
            print(f"✓ {model_name} saved to {filepath}")
        
        except Exception as e:
            print(f"✗ Error downloading {model_name}: {e}")
    
    def verify_models(self) -> bool:
        """Verify all models exist"""
        missing = []
        for model_name in self.MODELS.keys():
            filepath = os.path.join(self.model_dir, model_name)
            if not os.path.exists(filepath):
                missing.append(model_name)
        
        if missing:
            print(f"Missing models: {', '.join(missing)}")
            return False
        
        print("✓ All models verified!")
        return True

if __name__ == "__main__":
    downloader = ModelDownloader()
    downloader.download_all()
    downloader.verify_models()