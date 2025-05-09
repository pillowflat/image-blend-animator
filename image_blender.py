import numpy as np
from PIL import Image
import argparse
import os

def create_blended_gif(image1_path, image2_path, output_path, frames=30, duration=100, hold_start=2000, hold_end=5000):
    """
    Create an animated GIF that smoothly blends from image1 to image2
    
    Args:
        image1_path (str): Path to the first image
        image2_path (str): Path to the second image
        output_path (str): Path to save the output GIF
        frames (int): Number of frames in the transition (default: 30)
        duration (int): Duration of each frame in milliseconds (default: 100)
        hold_start (int): Time in milliseconds to hold on first image (default: 2000)
        hold_end (int): Time in milliseconds to hold on final image (default: 5000)
    """
    # Open the images
    img1 = Image.open(image1_path).convert('RGBA')
    img2 = Image.open(image2_path).convert('RGBA')
    
    # Check if images are very large
    max_dimension = 800  # Reasonable size for GIFs
    original_width = max(img1.width, img2.width)
    original_height = max(img1.height, img2.height)
    
    # Resize if too large
    if original_width > max_dimension or original_height > max_dimension:
        print(f"Images are large ({original_width}x{original_height}). Resizing for better performance.")
        # Calculate the scaling factor
        scale = min(max_dimension / original_width, max_dimension / original_height)
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        
        img1 = img1.resize((new_width, new_height), Image.LANCZOS)
        img2 = img2.resize((new_width, new_height), Image.LANCZOS)
        print(f"Resized to {new_width}x{new_height}")
    
    # Resize the smaller image to match the larger one
    width = max(img1.width, img2.width)
    height = max(img1.height, img2.height)
    
    img1 = img1.resize((width, height), Image.LANCZOS)
    img2 = img2.resize((width, height), Image.LANCZOS)
    
    # Convert images to numpy arrays
    img1_arr = np.array(img1, dtype=np.float32)
    img2_arr = np.array(img2, dtype=np.float32)
    
    # Create a list to store the frames
    frames_list = []
    
    # Helper function to add hold frames
    def add_hold_frames(image, hold_time_ms, frame_duration_ms):
        """Add additional frames to hold on an image for the specified time"""
        num_extra_frames = max(1, int(hold_time_ms / frame_duration_ms))
        return [image.copy() for _ in range(num_extra_frames)]
    
    # Add frames to hold on the first image
    first_frame = Image.fromarray(img1_arr.astype(np.uint8))
    start_hold_frames = add_hold_frames(first_frame, hold_start, duration)
    frames_list.extend(start_hold_frames)
    
    # Create the transition frames
    for i in range(frames + 1):
        # Calculate the blending factor (0 to 1)
        alpha = i / frames
        
        # Blend the images
        blended_arr = (1 - alpha) * img1_arr + alpha * img2_arr
        
        # Convert back to uint8 and then to PIL Image
        blended_img = Image.fromarray(blended_arr.astype(np.uint8))
        frames_list.append(blended_img)
    
    # Add frames to hold on the final image
    end_hold_frames = add_hold_frames(frames_list[-1], hold_end, duration)
    frames_list.extend(end_hold_frames)
    
    # Save as animated GIF
    print("Saving GIF... (this may take a moment)")
    try:
        # Convert RGBA to RGB if needed (can help with memory usage and compatibility)
        frames_rgb = [frame.convert('RGB') for frame in frames_list]
        
        # Save with optimization
        frames_rgb[0].save(
            output_path,
            format='GIF',
            append_images=frames_rgb[1:],
            save_all=True,
            duration=duration,
            loop=0,  # 0 means loop forever
            optimize=False  # Set to True for smaller file size, but slower processing
        )
        print(f"GIF created successfully and saved to {output_path}")
    except Exception as e:
        print(f"Error saving GIF: {e}")
        
        # Alternative saving method that might work better for large images
        print("Trying alternative saving method...")
        try:
            import imageio
            
            # Convert PIL images to numpy arrays
            images = [np.array(frame) for frame in frames_list]
            
            # Save using imageio
            imageio.mimsave(output_path, images, duration=duration/1000)
            print(f"GIF created successfully using imageio and saved to {output_path}")
        except ImportError:
            print("Could not use imageio as a fallback. Please install it: pip install imageio")
        except Exception as e:
            print(f"Error with alternative saving method: {e}")
            print("Try reducing image dimensions or number of frames.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a blending animation between two images")
    parser.add_argument("image1", help="Path to the first image")
    parser.add_argument("image2", help="Path to the second image")
    parser.add_argument("output", help="Path to save the output GIF")
    parser.add_argument("--frames", type=int, default=30, help="Number of frames (default: 30)")
    parser.add_argument("--duration", type=int, default=100, help="Duration of each frame in ms (default: 100)")
    parser.add_argument("--hold-start", type=int, default=2000, help="Time to hold on first image in ms (default: 2000)")
    parser.add_argument("--hold-end", type=int, default=5000, help="Time to hold on final image in ms (default: 5000)")
    
    args = parser.parse_args()
    
    create_blended_gif(args.image1, args.image2, args.output, 
                      args.frames, args.duration, 
                      args.hold_start, args.hold_end)