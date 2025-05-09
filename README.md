# Image Blend Animator

Image Blend Animator creates a smooth transition GIF that blends from one image to another. The tool offers customization for:
- Number of transition frames
- Frame duration
- Initial pause on the first image
- Final pause on the second image

This makes it perfect for creating engaging visual transitions for presentations, websites, or social media content.

## Examples

`python image_blender.py images/monkey_drawn.jpg images/monkey_ai.png images/monkey.gif --frames 100 --duration 40`

![Monkey](assets/monkey.png)

![Monkey - blended](assets/monkey_blend.gif)

`python image_blender.py images/monster_drawn.jpg images/monster_ai.png images/monster.gif --frames 100 --duration 40`

![Monster](assets/monster.png)

![Monster - blended](assets/monster_blend.gif)


## Features

- Smooth linear blending between two images
- Customizable number of transition frames for different smoothness levels
- Adjustable frame duration to control animation speed
- Configurable hold times at the beginning and end of the animation
- Automatic image resizing for better performance
- Error handling with fallback saving methods

## Installation

### Prerequisites

- Python 3.6 or higher

### Setup

1. Clone this repository or download the script:
   ```bash
   git clone https://github.com/pillowflat/image-blend-animator.git
   cd image-blend-animator
   ```

2. Make sure you have the required dependencies installed in a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate # Note: this command is slightly different for Windows
   pip install -r requirements.txt
   ```

## Prerequisites

### Generate the Photorealistic Version
Using OpenAI's DALL-E or any another AI image generation tool, upload your child's drawing and use the following prompt (or a prompt of your choice) to generate a photorealistic image based on the drawing.  Note that this prompt was not created by the author of this repository.  Also, the code for this repository is also 100% AI-generated using Anthropic's Sonnet 3.7 Large Language Model.

**The Prompt**
```text
"Take this drawing created by my child and transform it into a photorealistic image or realistic 3D render. 
I don't know what it's supposed to be it could be a creature, object, or something completely from their imagination. 
Keep the original shape, proportions, line lengths, and all imperfections exactly as they are in the drawing including any slanted eyes, 
uneven lines, or strange markings. Do not correct, smooth out, or change any details of their design. 
Make it look like this thing exists in the real world, with realistic textures (skin, fur, metal, etc.) and natural lighting. 
You can add realistic shadows and an environment or background that fits the feel of the drawing, 
but don't change anything about the form or details of what they created. 
No pencil crayon textures or hand-drawn styling. This must look like a photo or CGI render, but staying true to their imagination."

```

### Basic Usage

```bash
python image_blender.py path/to/first/image.jpg path/to/second/image.jpg output.gif
```

### Advanced Options

```bash
python image_blender.py path/to/first/image.jpg path/to/second/image.jpg output.gif \
  --frames 60 \
  --duration 50 \
  --hold-start 3000 \
  --hold-end 4000
```

### Parameters

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `image1` | Path to the first image | *Required* |
| `image2` | Path to the second image | *Required* |
| `output` | Path to save the output GIF | *Required* |
| `--frames` | Number of transition frames | 30 |
| `--duration` | Duration of each frame in milliseconds | 100 |
| `--hold-start` | Time to hold on first image in milliseconds | 2000 (2 seconds) |
| `--hold-end` | Time to hold on final image in milliseconds | 5000 (5 seconds) |

## Examples

### Slow Transition
```bash
python image_blender.py img1.jpg img2.jpg slow_transition.gif --frames 60 --duration 150
```

### Quick Flash
```bash
python image_blender.py img1.jpg img2.jpg quick_flash.gif --frames 10 --duration 50 --hold-start 500 --hold-end 500
```

### Presentation Slide
```bash
python image_blender.py slide1.png slide2.png presentation_transition.gif --hold-start 5000 --hold-end 8000
```

## Troubleshooting

### Memory Issues or Slow Performance

If you experience memory issues or slow performance:

1. Try using smaller images. The script automatically resizes images larger than 800px on their longest side, but you may want to pre-resize very large images.

2. Reduce the number of frames:
   ```bash
   python image_blender.py img1.jpg img2.jpg output.gif --frames 15
   ```

3. For large animations, the script will attempt to use the ImageIO library as a fallback if the PIL save method fails. Make sure you have ImageIO installed:
   ```bash
   pip install imageio
   ```

### File Format Issues

- Ensure your input images are in a format that PIL can read (JPG, PNG, BMP, etc.)
- If your output GIF has color issues, try using PNG files as input

## How It Works

The script works by:

1. Loading both input images
2. Resizing them to match dimensions (using the larger of the two)
3. Creating frames that are weighted averages between the images
4. Adding duplicate frames at the beginning and end for pause effects
5. Saving all frames as an animated GIF

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Pillow library for image processing
- NumPy for array operations
- ImageIO for alternative GIF saving