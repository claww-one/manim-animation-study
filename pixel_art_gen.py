import numpy as np
from PIL import Image, ImageDraw
import random
import math

# Image Config
WIDTH, HEIGHT = 320, 180  # Low res for Pixel Art feel
FRAMES = 30
OUTPUT_FILENAME = "lofi_pixel_art.gif"

def lerp_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

def generate_sky(width, height, t_offset):
    # Dynamic sunset gradient
    # Deep Purple -> Pink -> Orange
    colors = [
        (20, 10, 40),   # Deep Dark Night
        (60, 20, 60),   # Purple
        (200, 80, 80),  # Pinkish Red
        (250, 150, 50)  # Orange Sun
    ]
    
    pixels = np.zeros((height, width, 3), dtype=np.uint8)
    
    for y in range(height):
        # Calculate gradient position (0.0 to 1.0)
        # Add slight sine wave for "heat haze" or atmosphere movement
        y_norm = y / height
        shift = math.sin(y_norm * 5 + t_offset) * 0.05
        pos = np.clip(y_norm + shift, 0, 1) * (len(colors) - 1)
        
        idx = int(pos)
        t = pos - idx
        c = lerp_color(colors[idx], colors[min(idx+1, len(colors)-1)], t)
        pixels[y, :] = c
        
    return pixels

def add_stars(pixels, count=50, seed=42):
    rng = random.Random(seed)
    h, w, _ = pixels.shape
    for _ in range(count):
        x = rng.randint(0, w-1)
        y = rng.randint(0, h//2) # Stars only in upper half
        # Twinkle check could go here, but static stars for now
        if rng.random() > 0.1: 
            pixels[y, x] = (255, 255, 200)
    return pixels

def generate_mountains(width, height, seed=1):
    # 1D Noise for terrain
    rng = random.Random(seed)
    skyline = []
    y = height // 2 + 20
    for x in range(width):
        y += rng.uniform(-1.5, 1.5)
        # Pull back to center if too far
        if y < height // 2: y += 0.5
        if y > height - 40: y -= 0.5
        skyline.append(int(y))
    return skyline

def draw_scene(frame_idx):
    t = frame_idx / FRAMES * 2 * math.pi
    
    # 1. Base Sky
    pixels = generate_sky(WIDTH, HEIGHT, t)
    pixels = add_stars(pixels)
    
    # Convert to PIL for drawing shapes easily
    img = Image.fromarray(pixels)
    draw = ImageDraw.Draw(img)
    
    # 2. Sun (Retro style)
    # Sun moves slightly down
    sun_y = int(HEIGHT/2 + math.sin(t)*5)
    sun_x = int(WIDTH/2)
    sun_r = 30
    
    # Draw sun with scanlines (retro aesthetic)
    for y in range(sun_y - sun_r, sun_y + sun_r):
        if y % 4 == 0: continue # Scanline gap
        width_at_y = int(math.sqrt(sun_r**2 - (y - sun_y)**2))
        draw.line([(sun_x - width_at_y, y), (sun_x + width_at_y, y)], fill=(255, 200, 50))

    # 3. Mountains (Black Silhouette)
    skyline = generate_mountains(WIDTH, HEIGHT)
    # To smooth it slightly
    # Draw
    polygon = [(0, HEIGHT)] # Start bottom left
    for x, y in enumerate(skyline):
        polygon.append((x, y))
    polygon.append((WIDTH, HEIGHT)) # End bottom right
    
    draw.polygon(polygon, fill=(10, 5, 20))
    
    # 4. Water Reflection (The "Refined" part - pixel distortion)
    # Take the top half, flip it, distort x
    # For simplicity in PIL, let's just draw a reflective gradient overlay
    # Or actually manipulate pixels. Let's do a simple overlay.
    
    # Water surface area
    water_y = max(skyline)
    # Make water area distinct
    draw.rectangle([(0, HEIGHT-40), (WIDTH, HEIGHT)], fill=(20, 10, 40))
    
    # Add "glimmer" on water
    rng = random.Random(frame_idx)
    for _ in range(100):
        rx = rng.randint(0, WIDTH-1)
        ry = rng.randint(HEIGHT-40, HEIGHT-1)
        if rng.random() > 0.8:
            draw.point((rx, ry), fill=(100, 80, 150)) # Purple glimmer

    return img

# Generate Frames
images = []
print("Rendering frames...")
for i in range(FRAMES):
    img = draw_scene(i)
    # Scale up for visibility (Nearest Neighbor for pixel art look)
    img = img.resize((WIDTH*2, HEIGHT*2), Image.NEAREST)
    images.append(img)

# Save GIF
print(f"Saving {OUTPUT_FILENAME}...")
images[0].save(
    OUTPUT_FILENAME,
    save_all=True,
    append_images=images[1:],
    duration=100, # ms per frame
    loop=0
)
print("Done!")
