#!/usr/bin/env python3
"""
Image optimization script for personal-api website
Converts large PNG screenshots to optimized JPG files at multiple resolutions
"""

from PIL import Image
import os

# Define source images and their target names
images = [
    ("raw_images/img-2.32.36___PM.png", "jay-orange-jacket"),
    ("raw_images/img-2.34.16___PM.png", "jay-family-dandelion"),
    ("raw_images/img-2.36.00___PM.png", "jay-family-selfie"),
    ("raw_images/img-2.38.06___PM.png", "jay-family-theme-park"),
]

# Define output sizes (width in pixels)
sizes = [320, 640, 1200]

# Output directory
output_dir = "images"

def optimize_image(input_path, output_name):
    """
    Optimize a single image by creating multiple responsive versions
    """
    print(f"\nProcessing: {input_path}")

    # Open the image
    img = Image.open(input_path)

    # Convert RGBA to RGB if necessary (for PNG with transparency)
    if img.mode in ('RGBA', 'LA', 'P'):
        # Create a white background
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    # Get original dimensions
    orig_width, orig_height = img.size
    aspect_ratio = orig_height / orig_width

    print(f"  Original size: {orig_width}x{orig_height}")

    # Create versions at different sizes
    for width in sizes:
        # Calculate new height maintaining aspect ratio
        height = int(width * aspect_ratio)

        # Skip if the target size is larger than original
        if width > orig_width:
            print(f"  Skipping {width}w (larger than original)")
            continue

        # Resize image using high-quality Lanczos resampling
        resized = img.resize((width, height), Image.Resampling.LANCZOS)

        # Save as optimized JPG
        output_path = os.path.join(output_dir, f"{output_name}-{width}.jpg")
        resized.save(output_path, 'JPEG', quality=85, optimize=True)

        # Get file size
        file_size = os.path.getsize(output_path) / 1024  # KB
        print(f"  Created {width}w: {output_path} ({file_size:.1f} KB)")

def main():
    """
    Process all images
    """
    print("Starting image optimization...")
    print(f"Output directory: {output_dir}")

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Process each image
    for input_path, output_name in images:
        if os.path.exists(input_path):
            optimize_image(input_path, output_name)
        else:
            print(f"Warning: {input_path} not found, skipping...")

    print("\n✓ Image optimization complete!")

if __name__ == "__main__":
    main()
