#!/usr/bin/env python3
"""
Create a 5x5 grid blog cover image by sampling 25 images from the blog post.
Output: 4000x4000px image with square tiles (800x800px each).
"""

import re
from pathlib import Path
from PIL import Image
import random
import numpy as np

# Set random seed for reproducibility
random.seed(42)

# Configuration
MARKDOWN_FILE = "_posts/2025-12-25-how-to-hold-fibers.md"
OUTPUT_FILE = "assets/images/2025/20241224_20251225_long_thread/blog_cover_20251225.jpg"
GRID_SIZE = 5  # 5x5 grid
TILE_SIZE = 800  # Each tile is 800x800px
FINAL_SIZE = GRID_SIZE * TILE_SIZE  # 4000x4000px

def extract_image_paths(markdown_file):
    """Extract all image paths from the markdown file."""
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all image references in markdown format: ![alt](/path/to/image.jpg)
    pattern = r'!\[.*?\]\((.*?)\)'
    matches = re.findall(pattern, content)
    
    # Convert to absolute paths
    image_paths = []
    for match in matches:
        # Remove leading slash if present
        path = match.lstrip('/')
        image_paths.append(path)
    
    return image_paths

def crop_to_square(img):
    """Crop image to square by taking the center."""
    width, height = img.size
    size = min(width, height)

    left = (width - size) // 2
    top = (height - size) // 2
    right = left + size
    bottom = top + size

    return img.crop((left, top, right, bottom))

def calculate_white_percentage(img, threshold=250):
    """Calculate percentage of pixels that are close to pure white.

    Args:
        img: PIL Image in RGB mode
        threshold: RGB values above this are considered "white" (default 250)

    Returns:
        Percentage of white pixels (0-100)
    """
    # Convert to numpy array
    img_array = np.array(img)

    # Check if all RGB channels are above threshold
    white_mask = (img_array[:, :, 0] >= threshold) & \
                 (img_array[:, :, 1] >= threshold) & \
                 (img_array[:, :, 2] >= threshold)

    # Calculate percentage
    total_pixels = white_mask.size
    white_pixels = np.sum(white_mask)
    white_percentage = (white_pixels / total_pixels) * 100

    return white_percentage

def load_grid_info(grid_info_file):
    """Load grid info from file if it exists.

    Returns:
        Dictionary mapping (row, col) to filename, or None if file doesn't exist
    """
    if not Path(grid_info_file).exists():
        return None

    grid_info = {}
    with open(grid_info_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('(') and '):' in line:
                # Parse line like "(1,2): filename.jpg"
                pos_part, filename = line.split('): ')
                row, col = pos_part.strip('()').split(',')
                grid_info[(int(row), int(col))] = filename.strip()

    return grid_info

def save_grid_info(sampled_paths, output_file):
    """Save grid info to file."""
    grid_info_file = output_file.replace('.jpg', '_grid_info.txt')
    with open(grid_info_file, 'w') as f:
        f.write("Grid layout (row, col): filename\n")
        f.write("=" * 60 + "\n")
        for idx, img_path in enumerate(sampled_paths):
            row = idx // GRID_SIZE + 1
            col = idx % GRID_SIZE + 1
            f.write(f"({row},{col}): {img_path.split('/')[-1]}\n")
    print(f"Grid info saved to: {grid_info_file}")
    return grid_info_file

def load_blacklist(output_file):
    """Load blacklist from file if it exists.

    Returns:
        Set of blacklisted filenames
    """
    blacklist_file = output_file.replace('.jpg', '_blacklist.txt')
    if not Path(blacklist_file).exists():
        return set()

    blacklist = set()
    with open(blacklist_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                blacklist.add(line)

    return blacklist

def save_blacklist(blacklist, output_file):
    """Save blacklist to file."""
    blacklist_file = output_file.replace('.jpg', '_blacklist.txt')
    with open(blacklist_file, 'w') as f:
        f.write("# Blacklisted images (one per line)\n")
        for filename in sorted(blacklist):
            f.write(f"{filename}\n")
    print(f"Blacklist saved to: {blacklist_file}")

def create_cover_image(image_paths, output_file, white_threshold_percent=10.0, max_resample_attempts=5, manual_resample_positions=None):
    """Create a 5x5 grid cover image from sampled images.

    Args:
        image_paths: List of available image paths
        output_file: Path to save the output image
        white_threshold_percent: Maximum percentage of white pixels allowed (default 10%)
        max_resample_attempts: Maximum attempts to find a non-white image per position
        manual_resample_positions: List of (row, col) tuples (1-indexed) to manually resample
    """
    num_images_needed = GRID_SIZE * GRID_SIZE

    # Load existing grid info if available
    grid_info_file = output_file.replace('.jpg', '_grid_info.txt')
    existing_grid = load_grid_info(grid_info_file)

    # Load blacklist
    blacklist = load_blacklist(output_file)
    if blacklist:
        print(f"\nLoaded blacklist with {len(blacklist)} images")

    # If grid info exists, use it; otherwise sample new images
    if existing_grid:
        print(f"\nLoading existing grid from: {grid_info_file}")
        sampled_paths = []
        for row in range(1, GRID_SIZE + 1):
            for col in range(1, GRID_SIZE + 1):
                filename = existing_grid.get((row, col))
                if filename:
                    # Find the full path for this filename
                    full_path = next((p for p in image_paths if p.endswith(filename)), None)
                    if full_path:
                        sampled_paths.append(full_path)
                    else:
                        print(f"Warning: Could not find path for {filename}, resampling...")
                        sampled_paths.append(random.choice(image_paths))
                else:
                    print(f"Warning: No grid info for ({row},{col}), resampling...")
                    sampled_paths.append(random.choice(image_paths))
        print(f"Loaded {len(sampled_paths)} images from existing grid")
    else:
        # Sample 25 images randomly
        if len(image_paths) < num_images_needed:
            print(f"Warning: Only {len(image_paths)} images available, need {num_images_needed}")
            # Repeat images if necessary
            sampled_paths = random.choices(image_paths, k=num_images_needed)
        else:
            sampled_paths = random.sample(image_paths, num_images_needed)
        print(f"\nInitial selection: {len(sampled_paths)} images")

    # Manual resampling first (if specified)
    if manual_resample_positions:
        # Use a separate random generator for manual resampling to avoid affecting auto-resample
        manual_rng = random.Random(12345)  # Fixed seed for reproducibility

        print(f"\nManually resampling {len(manual_resample_positions)} positions:")
        for row, col in manual_resample_positions:
            idx = (row - 1) * GRID_SIZE + (col - 1)
            old_path = sampled_paths[idx]
            old_filename = old_path.split('/')[-1]

            # Add old image to blacklist
            blacklist.add(old_filename)
            print(f"  Added to blacklist: {old_filename}")

            # Try to find a new image that passes white threshold and is not a duplicate or blacklisted
            for attempt in range(max_resample_attempts * 3):  # More attempts for dedup
                # Exclude already used images (except the one we're replacing) and blacklisted images
                available = [p for p in image_paths
                           if (p not in sampled_paths or p == old_path)
                           and p.split('/')[-1] not in blacklist]
                if not available:
                    print(f"  Warning: No more images available for position ({row},{col})")
                    break

                new_path = manual_rng.choice(available)

                try:
                    # Check white percentage
                    img = Image.open(new_path)
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    white_pct = calculate_white_percentage(img)

                    if white_pct <= white_threshold_percent:
                        sampled_paths[idx] = new_path
                        print(f"  ✓ Position ({row},{col}): {old_filename} -> {new_path.split('/')[-1]} ({white_pct:.1f}% white)")
                        break
                    else:
                        # Remove from available and try again
                        if attempt < max_resample_attempts * 3 - 1:
                            continue
                        else:
                            print(f"  ⚠ Position ({row},{col}): Could not find image with <{white_threshold_percent}% white after {max_resample_attempts * 3} attempts")
                            sampled_paths[idx] = new_path
                            print(f"    Using: {new_path.split('/')[-1]} ({white_pct:.1f}% white)")
                except Exception as e:
                    print(f"  Error checking {new_path}: {e}")
                    break

        # Save updated blacklist
        save_blacklist(blacklist, output_file)

    print(f"\nChecking all images for >{white_threshold_percent}% white pixels...")

    # Check each image for white content and resample if needed (excluding manually resampled ones)
    manual_indices = set()
    if manual_resample_positions:
        manual_indices = {(row - 1) * GRID_SIZE + (col - 1) for row, col in manual_resample_positions}

    resampled_count = 0
    for idx in range(len(sampled_paths)):
        if idx in manual_indices:
            continue  # Skip manually resampled positions

        row = idx // GRID_SIZE + 1
        col = idx % GRID_SIZE + 1

        for attempt in range(max_resample_attempts * 3):  # More attempts for dedup
            img_path = sampled_paths[idx]

            try:
                # Load and check white percentage
                img = Image.open(img_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                white_pct = calculate_white_percentage(img)

                if white_pct <= white_threshold_percent:
                    # Image is good, keep it
                    if attempt > 0:
                        print(f"  ✓ Position ({row},{col}): {img_path.split('/')[-1]} - {white_pct:.1f}% white (OK after {attempt} resamples)")
                    break
                else:
                    # Too much white, resample
                    if attempt == 0:
                        print(f"  ✗ Position ({row},{col}): {img_path.split('/')[-1]} - {white_pct:.1f}% white (resampling...)")
                        resampled_count += 1

                    # Get a new random image that's not already used
                    available = [p for p in image_paths if p not in sampled_paths or p == img_path]
                    if available:
                        sampled_paths[idx] = random.choice(available)
                    else:
                        print(f"    Warning: No more images available, keeping current image")
                        break

            except Exception as e:
                print(f"  Error checking {img_path}: {e}")
                break

    print(f"\nAuto-resampled {resampled_count} images due to high white content")
    print(f"Final selection: {len(sampled_paths)} images for the cover")

    # Save grid info to file
    save_grid_info(sampled_paths, output_file)
    print()

    # Create blank canvas
    canvas = Image.new('RGB', (FINAL_SIZE, FINAL_SIZE), color='white')

    # Place images in grid
    for idx, img_path in enumerate(sampled_paths):
        row = idx // GRID_SIZE
        col = idx % GRID_SIZE

        try:
            # Load and process image
            img = Image.open(img_path)

            # Convert to RGB if necessary (handles RGBA, grayscale, etc.)
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Crop to square
            img = crop_to_square(img)

            # Resize to tile size
            img = img.resize((TILE_SIZE, TILE_SIZE), Image.Resampling.LANCZOS)

            # Paste onto canvas
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            canvas.paste(img, (x, y))

            print(f"  [{idx+1}/{num_images_needed}] Row {row+1}, Col {col+1}: {img_path.split('/')[-1]}")

        except Exception as e:
            print(f"  Error processing {img_path}: {e}")
            # Leave blank tile on error

    # Save the final image
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_file, 'JPEG', quality=95, optimize=True)
    print(f"\nCover image saved to: {output_file}")
    print(f"Final size: {FINAL_SIZE}x{FINAL_SIZE}px")

def main():
    print("Creating blog cover image...")
    print(f"Reading from: {MARKDOWN_FILE}")

    # Extract image paths
    image_paths = extract_image_paths(MARKDOWN_FILE)
    print(f"Found {len(image_paths)} images in the markdown file")

    # Manually resample specific positions (row, col) - 1-indexed
    # Note: User's convention is (col, row) so we flip them here
    # User specified: (2,1), (2,3), (4,5) which means col,row
    # manual_resample = [(2,1), (1, 2), (2,5), (3, 2), (5, 4), (4,5), (5,5)]  # Flipped to (row, col)
    manual_resample = [(4,5)]  # Flipped to (row, col)

    # Create cover image with automatic white content filtering
    # Images with >10% white pixels will be automatically resampled
    create_cover_image(image_paths, OUTPUT_FILE,
                      white_threshold_percent=5.0,
                      manual_resample_positions=manual_resample)

if __name__ == "__main__":
    main()

