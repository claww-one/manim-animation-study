import numpy as np
from PIL import Image, ImageDraw
import random
import math
import os

# Config - Higher Resolution for Finer Details
CANVAS_WIDTH = 160
CANVAS_HEIGHT = 120
SCALE = 4  # Lower scale multiplier since base res is higher
OUTPUT_DIR = "animal_pixels_refined"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Palette
BG_COLOR = (220, 235, 255) # Soft Sky Blue
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# --- Utilities ---
def create_canvas():
    return Image.new('RGB', (CANVAS_WIDTH, CANVAS_HEIGHT), BG_COLOR)

def save_gif(frames, filename, duration=120):
    # Scale up using Nearest Neighbor
    scaled_frames = [f.resize((CANVAS_WIDTH * SCALE, CANVAS_HEIGHT * SCALE), Image.NEAREST) for f in frames]
    scaled_frames[0].save(
        f"{OUTPUT_DIR}/{filename}",
        save_all=True,
        append_images=scaled_frames[1:],
        duration=duration,
        loop=0
    )
    print(f"Generated {filename}")

def draw_grass(draw):
    # Draw some ground
    draw.rectangle([0, CANVAS_HEIGHT-20, CANVAS_WIDTH, CANVAS_HEIGHT], fill=(100, 180, 100))
    # Blades
    rng = random.Random(42)
    for x in range(0, CANVAS_WIDTH, 4):
        h = rng.randint(2, 6)
        draw.line([x, CANVAS_HEIGHT-20, x, CANVAS_HEIGHT-20-h], fill=(80, 160, 80))

# --- 1. Refined Cat (Detailed Tabby) ---
def generate_cat_refined():
    frames = []
    num_frames = 12
    
    ORANGE = (230, 140, 50)
    STRIPE = (180, 100, 30)
    WHITE = (255, 255, 255)
    EYE_GREEN = (100, 200, 100)
    
    cx, cy = CANVAS_WIDTH//2, CANVAS_HEIGHT - 30
    
    for f in range(num_frames):
        img = create_canvas()
        draw = ImageDraw.Draw(img)
        draw_grass(draw)
        
        # Breathing
        breath = math.sin(f / num_frames * math.pi * 2)
        body_h = 35 + breath * 1
        
        # Tail (Sine wave)
        tail_offset = math.sin(f / num_frames * math.pi * 2) * 5
        # Tail base
        draw.line([cx+10, cy-5, cx+25, cy-10+tail_offset], fill=ORANGE, width=4)
        
        # Body (Sitting)
        draw.ellipse([cx-15, cy-body_h, cx+15, cy], fill=ORANGE)
        # Chest patch
        draw.ellipse([cx-8, cy-body_h+5, cx+8, cy-10], fill=WHITE)
        
        # Head
        head_y = cy - body_h - 15
        draw.ellipse([cx-12, head_y, cx+12, head_y+22], fill=ORANGE)
        
        # Stripes (Head)
        draw.line([cx-5, head_y+2, cx+5, head_y+2], fill=STRIPE, width=1)
        draw.line([cx-4, head_y+4, cx+4, head_y+4], fill=STRIPE, width=1)
        
        # Ears
        draw.polygon([(cx-10, head_y+5), (cx-14, head_y-5), (cx-4, head_y+5)], fill=ORANGE)
        draw.polygon([(cx+10, head_y+5), (cx+14, head_y-5), (cx+4, head_y+5)], fill=ORANGE)
        
        # Face details
        # Eyes
        if f in [5, 6]: # Blink
            draw.line([cx-8, head_y+12, cx-4, head_y+12], fill=(50,30,0), width=1)
            draw.line([cx+4, head_y+12, cx+8, head_y+12], fill=(50,30,0), width=1)
        else:
            draw.rectangle([cx-8, head_y+10, cx-4, head_y+13], fill=EYE_GREEN)
            draw.rectangle([cx+4, head_y+10, cx+8, head_y+13], fill=EYE_GREEN)
            # Pupils
            draw.point((cx-6, head_y+11), fill=(0,0,0))
            draw.point((cx+6, head_y+11), fill=(0,0,0))
            
        # Nose/Mouth
        draw.point((cx, head_y+16), fill="pink")
        draw.line([cx, head_y+16, cx-2, head_y+18], fill=(50,30,0), width=1)
        draw.line([cx, head_y+16, cx+2, head_y+18], fill=(50,30,0), width=1)
        
        # Whiskers (Fine lines)
        draw.line([cx-15, head_y+16, cx-8, head_y+17], fill=(200,200,200), width=1)
        draw.line([cx+15, head_y+16, cx+8, head_y+17], fill=(200,200,200), width=1)

        frames.append(img)
    
    save_gif(frames, "fine_cat.gif")

# --- 2. Refined Rabbit (Fluffy) ---
def generate_rabbit_refined():
    frames = []
    num_frames = 8 # Faster movement
    
    GREY_FUR = (200, 200, 210)
    DARK_GREY = (150, 150, 160)
    PINK = (255, 180, 190)
    
    cx, cy = CANVAS_WIDTH//2, CANVAS_HEIGHT - 30
    
    for f in range(num_frames):
        img = create_canvas()
        draw = ImageDraw.Draw(img)
        draw_grass(draw)
        
        # Eating animation (Head bob)
        bob = 0
        if f % 2 == 0: bob = 1
        
        # Body
        draw.ellipse([cx-12, cy-20, cx+12, cy], fill=GREY_FUR)
        # Tail
        draw.ellipse([cx+10, cy-10, cx+18, cy-2], fill=WHITE)
        
        # Head
        h_y = cy - 25 + bob
        draw.ellipse([cx-10, h_y, cx+8, h_y+16], fill=GREY_FUR)
        
        # Ears (Long)
        draw.ellipse([cx-8, h_y-15, cx-4, h_y+5], fill=GREY_FUR) # Left Back
        draw.ellipse([cx-2, h_y-15, cx+2, h_y+5], fill=GREY_FUR) # Right Front
        draw.ellipse([cx-1, h_y-12, cx+1, h_y], fill=PINK) # Inner
        
        # Face
        draw.rectangle([cx-6, h_y+8, cx-4, h_y+10], fill=(0,0,0)) # Eye
        
        # Nose/Chewing
        draw.point((cx+2, h_y+10+bob), fill=PINK)
        
        # Carrot
        draw.polygon([(cx+5, h_y+12+bob), (cx+15, h_y+10+bob), (cx+6, h_y+14+bob)], fill="orange")
        draw.line([cx+15, h_y+10+bob, cx+18, h_y+8+bob], fill="green", width=1)

        frames.append(img)
    
    save_gif(frames, "fine_rabbit.gif")

# --- 3. Refined Dog (Shiba Inu) ---
def generate_dog_refined():
    frames = []
    num_frames = 16
    
    TAN = (210, 160, 100)
    CREAM = (245, 235, 220)
    
    cx, cy = CANVAS_WIDTH//2, CANVAS_HEIGHT - 30
    
    for f in range(num_frames):
        img = create_canvas()
        draw = ImageDraw.Draw(img)
        draw_grass(draw)
        
        # Body
        draw.ellipse([cx-15, cy-25, cx+15, cy], fill=TAN)
        draw.ellipse([cx-8, cy-25, cx+8, cy-10], fill=CREAM) # Belly
        
        # Head
        h_y = cy - 35
        # Tilt head
        tilt = math.sin(f / num_frames * math.pi * 2) * 2
        
        draw.ellipse([cx-14+tilt, h_y, cx+14+tilt, h_y+24], fill=TAN)
        # Snout mask
        draw.ellipse([cx-8+tilt, h_y+12, cx+8+tilt, h_y+24], fill=CREAM)
        
        # Ears (Triangular)
        draw.polygon([(cx-10+tilt, h_y+5), (cx-14+tilt, h_y-4), (cx-6+tilt, h_y+5)], fill=TAN)
        draw.polygon([(cx+10+tilt, h_y+5), (cx+14+tilt, h_y-4), (cx+6+tilt, h_y+5)], fill=TAN)
        
        # Face
        draw.rectangle([cx-6+tilt, h_y+10, cx-3+tilt, h_y+13], fill=(0,0,0)) # L Eye
        draw.rectangle([cx+3+tilt, h_y+10, cx+6+tilt, h_y+13], fill=(0,0,0)) # R Eye
        draw.rectangle([cx-2+tilt, h_y+16, cx+2+tilt, h_y+19], fill=(0,0,0)) # Nose
        
        # Tongue (Pant)
        if f % 4 < 2:
            draw.ellipse([cx-2+tilt, h_y+20, cx+2+tilt, h_y+26], fill="pink")
            
        # Tail (Curly)
        draw.arc([cx+10, cy-20, cx+25, cy-5], start=180, end=360, fill=TAN, width=4)

        frames.append(img)
    
    save_gif(frames, "fine_dog.gif")

if __name__ == "__main__":
    generate_cat_refined()
    generate_rabbit_refined()
    generate_dog_refined()
