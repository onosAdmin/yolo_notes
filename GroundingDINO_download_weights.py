import os
import requests
from tqdm import tqdm
import torch

def download_file(url, destination):
    """
    Download a file from a URL to a destination with a progress bar
    """
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    
    if os.path.exists(destination):
        existing_size = os.path.getsize(destination)
        if existing_size == total_size and is_valid_pytorch_file(destination):
            print(f"File already exists and is valid: {destination}")
            return
        else:
            print(f"Existing file is incomplete or corrupted. Redownloading...")
            
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
    
    with open(destination, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    
    progress_bar.close()
    
    if total_size != 0 and progress_bar.n != total_size:
        print("ERROR, something went wrong with the download")
    else:
        print(f"Download complete: {destination}")

def is_valid_pytorch_file(file_path):
    """
    Check if a file is a valid PyTorch model file
    """
    try:
        # Try to load the file as a PyTorch model
        torch.load(file_path, map_location="cpu")
        return True
    except Exception:
        return False

if __name__ == "__main__":
    # GroundingDINO weights URL
    weights_url = "https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth"
    
    # Set the destination path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    weights_path = os.path.join(script_dir, "weights", "groundingdino_swint_ogc.pth")
    
    # Download the weights
    print(f"Downloading GroundingDINO weights to {weights_path}")
    download_file(weights_url, weights_path)
    
    # Verify the download
    if is_valid_pytorch_file(weights_path):
        print("✅ The model file is valid and ready to use.")
    else:
        print("❌ The model file is still corrupted after download. Please check your internet connection and try again.")
