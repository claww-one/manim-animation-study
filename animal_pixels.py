import numpy as np
from PIL import Image, ImageDraw
import random
import math
import os

# Config
CANVAS_SIZE = 64
SCALE = 8
OUTPUT_DIR = "animal_pixels"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Palette
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (200, 220, 255) # Light Blue

# --- Utilities ---
def create_canvas():
    return Image.new('RGB', (CANVAS_SIZE, CANVAS_SIZE), BG_COLOR)

def save_gif(frames, filename, duration=150):
    # Scale up using Nearest Neighbor to preserve pixel look
    scaled_frames = [f.resize((CANVAS_SIZE * SCALE, CANVAS_SIZE * SCALE), Image.NEAREST) for f in frames]
    scaled_frames[0].save(
        f"{OUTPUT_DIR}/{filename}",
        save_all=True,
        append_images=scaled_frames[1:],
        duration=duration,
        loop=0
    )
    print(f"Generated {filename}")

# --- 1. Cat (Orange Tabby) ---
def generate_cat():
    frames = []
    num_frames = 10
    
    ORANGE = (255, 165, 0)
    DARK_ORANGE = (200, 100, 0)
    
    for f in range(num_frames):
        img = create_canvas()
        draw = ImageDraw.Draw(img)
        
        # Body
        draw.rectangle([20, 30, 44, 50], fill=ORANGE)
        
        # Head
        draw.rectangle([22, 18, 42, 32], fill=ORANGE)
        
        # Ears
        draw.polygon([(22, 18), (25, 10), (28, 18)], fill=ORANGE) # Left
        draw.polygon([(36, 18), (39, 10), (42, 18)], fill=ORANGE) # Right
        
        # Eyes (Blink)
        if f in [4, 5]: # Blink
            draw.line([25, 24, 28, 24], fill=BLACK, width=1)
            draw.line([36, 24, 39, 24], fill=BLACK, width=1)
        else:
            draw.rectangle([25, 23, 27, 25], fill=BLACK)
            draw.rectangle([36, 23, 38, 25], fill=BLACK)
            
        # Nose
        draw.rectangle([31, 27, 33, 28], fill="pink")
        
        # Tail (Wag)
        offset = math.sin(f / num_frames * math.pi * 2) * 3
        tail_tip = 44 + int(offset)
        # Simple tail curve
        draw.line([44, 45, tail_tip, 40], fill=DARK_ORANGE, width=3)
        
        frames.append(img)
    
    save_gif(frames, "pixel_cat.gif")

# --- 2. Rabbit (White Bunny) ---
def generate_rabbit():
    frames = []
    num_frames = 8
    
    FUR = (250, 250, 250)
    PINK = (255, 192, 203)
    
    for f in range(num_frames):
        img = create_canvas()
        draw = ImageDraw.Draw(img)
        
        # Body (Round)
        draw.ellipse([20, 30, 44, 50], fill=FUR)
        
        # Head
        draw.ellipse([22, 15, 42, 35], fill=FUR)
        
        # Ears (Twitch)
        ear_offset = 0
        if f in [2, 3]: ear_offset = 2 # Twitch down
        
        # Left Ear
        draw.ellipse([22, 5+ear_offset, 28, 20+ear_offset], fill=FUR)
        draw.ellipse([24, 8+ear_offset, 26, 18+ear_offset], fill=PINK)
        
        # Right Ear
        draw.ellipse([36, 5, 42, 20], fill=FUR)
        draw.ellipse([38, 8, 40, 18], fill=PINK)
        
        # Eyes
        draw.rectangle([26, 22, 28, 24], fill=BLACK)
        draw.rectangle([36, 22, 38, 24], fill=BLACK)
        
        # Nose (Wiggle)
        nose_y = 28
        if f % 2 == 0: nose_y -= 1
        draw.rectangle([31, nose_y, 33, nose_y+1], fill=PINK)
        
        frames.append(img)
        
    save_gif(frames, "pixel_rabbit.gif")

# --- 3. Dog (Beagle style) ---
def generate_dog():
    frames = []
    num_frames = 8
    
    BROWN = (139, 69, 19)
    WHITE = (255, 255, 255)
    
    for f in range(num_frames):
        img = create_canvas()
        draw = ImageDraw.Draw(img)
        
        # Body
        draw.rectangle([20, 35, 44, 50], fill=WHITE)
        draw.rectangle([20, 35, 30, 50], fill=BROWN) # Spot
        
        # Head
        draw.rectangle([22, 20, 42, 35], fill=BROWN)
        draw.rectangle([28, 20, 36, 35], fill=WHITE) # Stripe
        
        # Ears (Floppy)
        # Bounce effect
        bounce = 0
        if f % 2 == 0: bounce = 1
        
        draw.rectangle([18, 22+bounce, 22, 32+bounce], fill=BROWN) # Left
        draw.rectangle([42, 22+bounce, 46, 32+bounce], fill=BROWN) # Right
        
        # Eyes
        draw.rectangle([26, 25, 28, 27], fill=BLACK)
        draw.rectangle([36, 25, 38, 27], fill=BLACK)
        
        # Tongue (Pant)
        if f % 2 == 0:
            draw.rectangle([30, 32, 34, 36], fill="red") # Out
        
        # Tail (Fast Wag)
        tail_x = 20
        if f % 2 == 0: tail_x -= 2
        draw.line([20, 40, tail_x, 30], fill=WHITE, width=2)
        
        frames.append(img)
        
    save_gif(frames, "pixel_dog.gif")

if __name__ == "__main__":
    generate_cat()
    generate_rabbit()
    generate_dog()
