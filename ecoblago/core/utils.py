from PIL import Image
from typing import Tuple


def get_cropped_image(image: Image.Image, target_ratio: float) -> Image.Image:
    """
    Crop an image to the specified aspect ratio while maintaining the center.
    
    Args:
        image (PIL.Image.Image): The input image to crop
        target_ratio (float): The target aspect ratio (width/height)
        
    Returns:
        PIL.Image.Image: The cropped image with the specified aspect ratio
    """
    width, height = image.size
    current_ratio = width / height
    
    if current_ratio > target_ratio:
        new_width = int(height * target_ratio)
        new_height = height
        left = (width - new_width) // 2
        top = 0
        right = left + new_width
        bottom = height
    else:
        new_width = width
        new_height = int(width / target_ratio)
        left = 0
        top = (height - new_height) // 2
        right = width
        bottom = top + new_height
    
    return image.crop((left, top, right, bottom))
