import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import random
import math
import os

# Config
WIDTH, HEIGHT = 400, 400
OUTPUT_DIR = "cartoon_style"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- Cartoon Drawing Utilities ---

def draw_blob(draw, x, y, size, color, seed=None):
    """Draws an organic 'blob' shape commonly found in modern flat cartoons."""
    if seed: random.seed(seed)
    points = []
    num_points = 8
    for i in range(num_points):
        angle = (i / num_points) * 2 * math.pi
        # Vary radius for organic feel
        r = size * (0.8 + random.random() * 0.4)
        px = x + math.cos(angle) * r
        py = y + math.sin(angle) * r
        points.append((px, py))
    
    # Smooth points (Chaikin's algorithm or just draw polygon for now, PIL curve is tricky)
    # Using polygon for "cut-out" style
    draw.polygon(points, fill=color, outline=None)

def draw_eye(draw, x, y, size, look_at=(0,0)):
    """Draws a cartoon eye with pupil looking at target."""
    # Sclera (White)
    draw.ellipse([x-size, y-size, x+size, y+size], fill="white", outline="black", width=2)
    
    # Pupil (Black)
    pupil_size = size * 0.4
    # Vector to look_at
    dx, dy = look_at[0]-x, look_at[1]-y
    dist = math.sqrt(dx*dx + dy*dy)
    offset_dist = min(dist, size - pupil_size - 2) # Keep inside
    if dist > 0:
        offset_x = (dx/dist) * offset_dist
        offset_y = (dy/dist) * offset_dist
    else:
        offset_x, offset_y = 0, 0
        
    px, py = x + offset_x, y + offset_y
    draw.ellipse([px-pupil_size, py-pupil_size, px+pupil_size, py+pupil_size], fill="black")
    
    # Shine (Reflection)
    shine_size = pupil_size * 0.4
    draw.ellipse([px+pupil_size*0.2, py-pupil_size*0.5, px+pupil_size*0.2+shine_size, py-pupil_size*0.5+shine_size], fill="white")

# --- Scene: The "Blobby" Character ---
def generate_cartoon_character(frames=20):
    images = []
    
    # Palette (Pastel/Flat)
    BG_COLOR = "#FFD1DC" # Pinkish
    BODY_COLOR = "#87CEEB" # Sky Blue
    SHADOW_COLOR = "#5F9EA0" # Darker Blue
    
    # Interaction Target (A flying fly)
    fly_x, fly_y = WIDTH//2, HEIGHT//2
    
    for f in range(frames):
        img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
        draw = ImageDraw.Draw(img)
        
        t = f / frames * 2 * math.pi
        
        # 1. Fly Movement (Figure 8)
        fly_x = WIDTH//2 + math.cos(t) * 100
        fly_y = HEIGHT//2 - 100 + math.sin(t*2) * 50
        
        # Draw Fly trail
        draw.line([fly_x-5, fly_y, fly_x+5, fly_y], fill="black", width=1)
        draw.ellipse([fly_x-2, fly_y-2, fly_x+2, fly_y+2], fill="black")
        
        # 2. Character Body (Squash and Stretch)
        # Bouncing beat
        bounce = abs(math.sin(t))
        squash_x = 1.0 + (0.1 * bounce)
        squash_y = 1.0 - (0.1 * bounce)
        
        cx, cy = WIDTH//2, HEIGHT - 80
        radius = 80
        
        # Simple transform simulation by drawing oval
        w = radius * squash_x
        h = radius * squash_y
        
        # Shadow underneath
        draw.ellipse([cx-w*0.8, cy+h-10, cx+w*0.8, cy+h+10], fill="#E5B7C2")
        
        # Main Body
        draw.ellipse([cx-w, cy-h, cx+w, cy+h], fill=BODY_COLOR, outline="black", width=3)
        
        # Face (Eyes tracking fly)
        eye_spacing = 30 * squash_x
        eye_y = cy - 20 * squash_y
        
        draw_eye(draw, cx - eye_spacing, eye_y, 20, (fly_x, fly_y))
        draw_eye(draw, cx + eye_spacing, eye_y, 20, (fly_x, fly_y))
        
        # Mouth (Simple Arc)
        draw.arc([cx-10, cy+10, cx+10, cy+30], start=0, end=180, fill="black", width=2)

        images.append(img)

    images[0].save(f"{OUTPUT_DIR}/blobby_cartoon.gif", save_all=True, append_images=images[1:], duration=100, loop=0)
    print("Generated blobby_cartoon.gif")

if __name__ == "__main__":
    generate_cartoon_character()
