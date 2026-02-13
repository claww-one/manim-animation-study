import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import random
import math
import os

# Config - High Quality Flow Field
WIDTH, HEIGHT = 480, 270
SCALE = 1
FRAMES = 60
PARTICLE_COUNT = 4000
OUTPUT_DIR = "artistic_gen"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

class Particle:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.vx = 0
        self.vy = 0
        # Color based on position (Nebula gradient)
        self.color = self.get_color()
        self.age = 0
        self.max_age = random.uniform(20, 60)

    def get_color(self):
        # Center is Cyan, Edges are Magenta/Purple
        dist = math.sqrt((self.x - WIDTH/2)**2 + (self.y - HEIGHT/2)**2)
        norm_dist = min(dist / (WIDTH/2), 1.0)
        
        # Cyan (0, 255, 255) -> Purple (150, 0, 200)
        r = int(0 * (1-norm_dist) + 150 * norm_dist)
        g = int(255 * (1-norm_dist) + 0 * norm_dist)
        b = int(255 * (1-norm_dist) + 200 * norm_dist)
        return (r, g, b)

    def update(self, flow_grid, cols, rows):
        # Map pos to grid
        c = int(self.x / 10)
        r = int(self.y / 10)
        if c >= 0 and c < cols and r >= 0 and r < rows:
            angle = flow_grid[r][c]
            # Accelerate in direction
            self.vx += math.cos(angle) * 0.5
            self.vy += math.sin(angle) * 0.5
            
        # Friction
        self.vx *= 0.8
        self.vy *= 0.8
        
        self.x += self.vx
        self.y += self.vy
        self.age += 1
        
        # Respawn if out of bounds or too old
        if (self.x < 0 or self.x > WIDTH or 
            self.y < 0 or self.y > HEIGHT or 
            self.age > self.max_age):
            self.reset()

def get_flow_grid(t):
    cols = WIDTH // 10 + 1
    rows = HEIGHT // 10 + 1
    grid = np.zeros((rows, cols))
    
    # Complex trigonometry for "organic" flow without external noise lib
    for r in range(rows):
        for c in range(cols):
            # 3-Layer wave interference
            val = math.sin(c * 0.1 + t) * math.cos(r * 0.1 + t/2)
            val += math.sin(c * 0.3 - t) * 0.5
            val += math.cos(r * 0.2 + c * 0.2) * 0.3
            
            # Map to angle (0 - 2PI)
            grid[r][c] = val * math.pi * 2
    return grid, cols, rows

def generate_flow_field_art():
    print("Generating Flow Field Animation...")
    particles = [Particle() for _ in range(PARTICLE_COUNT)]
    
    images = []
    # Use a persistent canvas for "trails" effect
    canvas = Image.new('RGB', (WIDTH, HEIGHT), (5, 5, 10))
    
    for f in range(FRAMES):
        # 1. Fade previous frame slightly (Trails effect)
        # Convert to numpy to multiply opacity
        arr = np.array(canvas).astype(float)
        arr *= 0.9  # Fade factor (Keep 90% of previous image)
        canvas = Image.fromarray(arr.astype(np.uint8))
        draw = ImageDraw.Draw(canvas)
        
        # 2. Update Vector Field
        t = f * 0.1
        grid, cols, rows = get_flow_grid(t)
        
        # 3. Update & Draw Particles
        for p in particles:
            prev_x, prev_y = p.x, p.y
            p.update(grid, cols, rows)
            
            # Draw line segment
            # Opacity based on age (fade in/out)
            alpha = int(255 * math.sin(p.age / p.max_age * math.pi))
            if alpha > 0:
                # Add "bloom" pixel
                draw.line([prev_x, prev_y, p.x, p.y], fill=p.color, width=1)
        
        # 4. Final Polish: Mild Blur/Glow simulation
        # Only save every frame directly
        images.append(canvas.copy())

    output_path = f"{OUTPUT_DIR}/nebula_flow.gif"
    images[0].save(output_path, save_all=True, append_images=images[1:], duration=60, loop=0)
    print(f"Saved {output_path}")

if __name__ == "__main__":
    generate_flow_field_art()
