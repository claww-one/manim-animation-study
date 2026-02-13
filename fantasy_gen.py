import numpy as np
from PIL import Image, ImageDraw
import random
import math
import os

# Config
WIDTH, HEIGHT = 320, 180
SCALE = 2
OUTPUT_DIR = "fantasy_art"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- Utilities ---
def lerp_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

def smooth_noise(x, seed):
    random.seed(seed)
    # Simple 1D noise smoothing
    i = int(x)
    f = x - i
    v1 = random.random()
    random.seed(seed + 1)
    v2 = random.random()
    return v1 * (1-f) + v2 * f

# --- Scene 1: Floating Sky Island (Fantasy) ---
def generate_sky_island(frames=30):
    images = []
    for f in range(frames):
        # Soft Pastel Sky (Pink -> Blue)
        img = Image.new('RGB', (WIDTH, HEIGHT))
        pixels = img.load()
        
        for y in range(HEIGHT):
            t = y / HEIGHT
            col = lerp_color((135, 206, 235), (255, 182, 193), t) # SkyBlue -> LightPink
            for x in range(WIDTH):
                pixels[x, y] = col
        
        draw = ImageDraw.Draw(img)
        
        # Floating Island
        t_float = math.sin(f / frames * 2 * math.pi) * 5 # Bobbing up and down
        ix, iy = WIDTH//2, HEIGHT//2 + int(t_float)
        
        # Island Base (Green top, Brown bottom)
        draw.ellipse([ix-40, iy-20, ix+40, iy+20], fill=(100, 200, 100)) # Grass
        draw.polygon([(ix-30, iy+10), (ix+30, iy+10), (ix, iy+50)], fill=(100, 70, 50)) # Earth spike
        
        # Magical Tree
        tx, ty = ix, iy-10
        draw.rectangle([tx-3, ty-30, tx+3, ty], fill=(80, 50, 30)) # Trunk
        # Glowing Leaves
        leaf_color = lerp_color((255, 100, 200), (200, 100, 255), (math.sin(f/5)+1)/2)
        draw.ellipse([tx-20, ty-50, tx+20, ty-20], fill=leaf_color)
        
        # Falling Petals (Particles)
        for p in range(10):
            px = ix + math.sin(p*13 + f*0.1) * 30
            py = iy - 30 + (f*2 + p*10) % 80
            draw.point((px, py), fill=(255, 200, 220))

        # Clouds (White fluffy)
        for c in range(3):
            cx = (c * 100 + f) % (WIDTH + 100) - 50
            cy = 40 + c * 30
            draw.ellipse([cx, cy, cx+60, cy+30], fill=(255, 255, 255, 200))

        images.append(img.resize((WIDTH*SCALE, HEIGHT*SCALE), Image.NEAREST))
    
    images[0].save(f"{OUTPUT_DIR}/sky_island.gif", save_all=True, append_images=images[1:], duration=100, loop=0)
    print("Generated sky_island.gif")

# --- Scene 2: Crystal Cave (Magical) ---
def generate_crystal_cave(frames=20):
    images = []
    for f in range(frames):
        # Dark Cave BG
        img = Image.new('RGB', (WIDTH, HEIGHT), (20, 10, 30))
        draw = ImageDraw.Draw(img)
        
        # Crystals
        crystals = [
            (50, 140, 20, (0, 255, 255)), # Cyan
            (160, 130, 30, (255, 0, 255)), # Magenta
            (270, 150, 25, (100, 255, 100)) # Green
        ]
        
        for i, (cx, cy, h, color) in enumerate(crystals):
            # Pulse glow
            pulse = (math.sin(f/frames * 2 * math.pi + i) + 1) / 2
            glow_radius = 10 + pulse * 10
            
            # Draw Glow (Soft circle behind)
            # PIL doesn't do soft gradients easily, use multiple circles
            for r in range(int(glow_radius), 0, -2):
                alpha = int(50 * (1 - r/glow_radius))
                # Note: PIL default draw doesn't support alpha on RGB image directly without RGBA conversion
                # Simulating with solid rings for pixel art style
                pass 
            
            # Crystal Shape
            poly = [
                (cx, cy-h),
                (cx+10, cy-h+10),
                (cx+10, cy),
                (cx-10, cy),
                (cx-10, cy-h+10)
            ]
            draw.polygon(poly, fill=color)
            
            # Sparkles
            if f % 10 == i * 3 % 10:
                sx = cx + random.randint(-15, 15)
                sy = cy - h/2 + random.randint(-15, 15)
                draw.line([sx-2, sy, sx+2, sy], fill=(255, 255, 255), width=1)
                draw.line([sx, sy-2, sx, sy+2], fill=(255, 255, 255), width=1)

        # Stalactites (Top)
        draw.polygon([(0,0), (WIDTH, 0), (WIDTH, 30), (0, 30)], fill=(10, 5, 15))
        for i in range(0, WIDTH, 20):
            draw.polygon([(i, 0), (i+20, 0), (i+10, random.randint(20, 50))], fill=(10, 5, 15))

        images.append(img.resize((WIDTH*SCALE, HEIGHT*SCALE), Image.NEAREST))

    images[0].save(f"{OUTPUT_DIR}/crystal_cave.gif", save_all=True, append_images=images[1:], duration=150, loop=0)
    print("Generated crystal_cave.gif")

if __name__ == "__main__":
    generate_sky_island()
    generate_crystal_cave()
