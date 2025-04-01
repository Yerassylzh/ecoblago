import os
import sys
import django
from PIL import Image
from core.utils import crop_image_to_ratio

from catalog.models import GalleryImage


def is_product_image(file_path: str) -> bool:
    """
    Check if the given file is a product image by checking if it exists in the GalleryImage model.
    
    Args:
        file_path (str): Full path to the file
        
    Returns:
        bool: True if the file is a product image, False otherwise
    """
    # Get the relative path from media_v2/uploads
    try:
        relative_path = file_path[file_path.rfind('\\') + 1:]
        return GalleryImage.objects.filter(image=f'uploads/{relative_path}').exists()
    except (IndexError, ValueError):
        return False


def crop_product_images(target_ratio: float = 1.0):
    """
    Crops all product images in media/uploads directory to a specific aspect ratio.
    
    Args:
        target_ratio (float): The target aspect ratio (width/height) for the cropped images.
                            Default is 1.0 (square)
    """
    # Get the project root directory (where manage.py is located)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    uploads_dir = os.path.join(project_root, 'media', 'uploads')
    
    if not os.path.exists(uploads_dir):
        print(f'Error: Directory {uploads_dir} does not exist')
        return
    
    processed_count = 0
    error_count = 0
    skipped_count = 0
    
    print(f'Starting to process images in {uploads_dir}')
    print(f'Target aspect ratio: {target_ratio}')
    
    for root, dirs, files in os.walk(uploads_dir):
        for file in files:
            file_path = os.path.join(root, file)
    
            if not is_product_image(file_path):
                skipped_count += 1
                print("NOT proccessed:", file_path)
                if skipped_count % 100 == 0:
                    print(f'Skipped {skipped_count} non-product images...')
                continue
            
            try:
                with Image.open(file_path) as img:
                    # Convert to RGB if necessary (for PNG with transparency)
                    if img.mode in ('RGBA', 'LA'):
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1])
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Crop the image
                    cropped_img = crop_image_to_ratio(img, target_ratio)
                    
                    # Save the cropped image back to the same location
                    cropped_img.save(file_path, quality=100)
                    processed_count += 1
                    
                    if processed_count % 10 == 0:
                        print(f'Processed {processed_count} product images...')
                        
            except Exception as e:
                error_count += 1
                print(f'Error processing {file}: {str(e)}')
    
    print(f'Finished processing images:')
    print(f'- Successfully processed: {processed_count}')
    print(f'- Skipped (non-product): {skipped_count}')
    print(f'- Errors: {error_count}')


def run():
    print("HERE")
    target_ratio: float = 416 / 312
    crop_product_images(target_ratio)
