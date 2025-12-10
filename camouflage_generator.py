import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.colors import ListedColormap
import random
from PIL import Image
from sklearn.cluster import KMeans
import os

def extract_dominant_colors(image_path, num_colors=4):
    """
    Extract dominant colors from an image using K-means clustering
    
    Args:
        image_path: Path to the image file
        num_colors: Number of dominant colors to extract
    
    Returns:
        List of hex color codes
    """
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return None
    
    try:
        # Load image
        img = Image.open(image_path)
        img = img.convert('RGB')
        
        # Resize for faster processing
        img.thumbnail((200, 200))
        
        # Convert to numpy array
        img_array = np.array(img)
        pixels = img_array.reshape(-1, 3)
        
        # Use K-means to find dominant colors
        kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        # Get cluster centers (dominant colors)
        colors = kmeans.cluster_centers_.astype(int)
        
        # Convert to hex
        hex_colors = ['#{:02x}{:02x}{:02x}'.format(r, g, b) for r, g, b in colors]
        
        print(f"\nExtracted {num_colors} dominant colors from {image_path}:")
        for i, color in enumerate(hex_colors, 1):
            print(f"  Color {i}: {color}")
        
        return hex_colors
    
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def generate_woodland_camo(width=800, height=600, num_patches=150, colors=None):
    """Generate woodland camouflage pattern"""
    fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
    
    # Use provided colors or default woodland palette
    if colors is None:
        colors = ['#3d4a2c', '#5a6b47', '#7a8a5e', '#2b3320']
    
    # Base color
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_facecolor(colors[2])
    
    # Generate random organic patches
    for _ in range(num_patches):
        # Random center point
        cx = random.uniform(0, width)
        cy = random.uniform(0, height)
        
        # Random size
        size = random.uniform(20, 80)
        
        # Create irregular blob
        angles = np.linspace(0, 2*np.pi, random.randint(6, 12))
        radii = [size * random.uniform(0.5, 1.5) for _ in angles]
        
        points = [(cx + r * np.cos(a), cy + r * np.sin(a)) 
                  for r, a in zip(radii, angles)]
        
        # Add patch
        color = random.choice(colors)
        patch = Polygon(points, facecolor=color, edgecolor='none', alpha=0.8)
        ax.add_patch(patch)
    
    ax.axis('off')
    plt.tight_layout(pad=0)
    return fig

def generate_digital_camo(width=800, height=600, pixel_size=15, colors=None):
    """Generate digital/pixelated camouflage pattern"""
    fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
    
    # Use provided colors or default digital camo palette
    if colors is None:
        colors = ['#b5a286', '#8d7e6a', '#6b5d4f', '#d4c4a8']
    
    # Create grid
    rows = height // pixel_size
    cols = width // pixel_size
    
    # Generate random pattern with some clustering
    pattern = np.random.choice(len(colors), size=(rows, cols))
    
    # Apply smoothing for clusters
    for _ in range(3):
        for i in range(1, rows-1):
            for j in range(1, cols-1):
                if random.random() < 0.3:
                    neighbors = [pattern[i-1, j], pattern[i+1, j], 
                               pattern[i, j-1], pattern[i, j+1]]
                    pattern[i, j] = max(set(neighbors), key=neighbors.count)
    
    cmap = ListedColormap(colors)
    ax.imshow(pattern, cmap=cmap, interpolation='nearest')
    ax.axis('off')
    plt.tight_layout(pad=0)
    return fig

def generate_tiger_stripe(width=800, height=600, num_stripes=35, colors=None):
    """Generate tiger stripe camouflage pattern similar to reference image"""
    fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
    
    # Use provided colors or default tiger stripe colors with black
    if colors is None:
        base_colors = ['#c17a3a', '#8b5a2b', '#f5deb3']  # orange, brown, cream
        black = '#000000'
    else:
        # Sort colors by brightness to identify lightest for background
        base_colors = colors.copy()
        black = '#000000'
    
    # Set light background color
    if colors and len(colors) > 0:
        # Use lightest color as background
        ax.set_facecolor(base_colors[-1] if len(base_colors) > 2 else base_colors[0])
    else:
        ax.set_facecolor('#f5deb3')  # cream background
    
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    
    # First layer: organic brown/orange blobs
    num_blobs = random.randint(40, 60)
    for _ in range(num_blobs):
        cx = random.uniform(-width*0.1, width*1.1)
        cy = random.uniform(-height*0.1, height*1.1)
        
        # Create irregular organic shape
        num_points = random.randint(8, 15)
        angles = np.linspace(0, 2*np.pi, num_points)
        base_size = random.uniform(40, 120)
        
        radii = []
        for i, angle in enumerate(angles):
            # More variation for organic look
            r = base_size * random.uniform(0.4, 1.6)
            radii.append(r)
        
        points = [(cx + r * np.cos(a), cy + r * np.sin(a)) 
                  for r, a in zip(radii, angles)]
        
        # Use brown/orange colors, not black
        if colors and len(base_colors) > 1:
            color = random.choice(base_colors[:-1])  # Exclude lightest
        else:
            color = random.choice(['#c17a3a', '#8b5a2b'])
        
        patch = Polygon(points, facecolor=color, edgecolor='none', alpha=0.9)
        ax.add_patch(patch)
    
    # Second layer: Bold black stripes on top
    for _ in range(num_stripes):
        # Random angle for variety
        angle = random.uniform(-30, 30)  # Mostly diagonal
        
        # Starting position
        if random.random() < 0.5:
            # Diagonal from top-left to bottom-right
            start_x = random.uniform(-width*0.3, width*0.7)
            start_y = random.uniform(-height*0.2, height*0.3)
        else:
            # More vertical variation
            start_x = random.uniform(-width*0.2, width*1.2)
            start_y = random.uniform(-height*0.3, height*0.5)
        
        # Create curvy stripe path
        num_segments = random.randint(15, 30)
        stripe_length = random.uniform(height*1.2, height*1.8)
        
        path_x = [start_x]
        path_y = [start_y]
        
        for i in range(num_segments):
            # Progress along stripe
            t = i / num_segments
            
            # Base diagonal movement
            next_y = start_y + stripe_length * t
            next_x = start_x + (stripe_length * t) * np.tan(np.radians(angle))
            
            # Add organic curves
            wave_offset = random.uniform(20, 60) * np.sin(t * random.uniform(3, 8) + random.uniform(0, 2*np.pi))
            next_x += wave_offset
            
            # Random jitter for organic feel
            next_x += random.uniform(-15, 15)
            next_y += random.uniform(-10, 10)
            
            path_x.append(next_x)
            path_y.append(next_y)
        
        # Create thick stripe with varying width
        base_width = random.uniform(20, 50)
        
        for i in range(len(path_x)-1):
            # Variable width along stripe
            width_factor = 1 + 0.4 * np.sin(i * 0.5)
            w = base_width * width_factor
            
            # Calculate perpendicular offset
            dx = path_x[i+1] - path_x[i]
            dy = path_y[i+1] - path_y[i]
            length = np.sqrt(dx**2 + dy**2)
            
            if length > 0:
                perp_x = -dy / length * w / 2
                perp_y = dx / length * w / 2
                
                points = [
                    (path_x[i] + perp_x, path_y[i] + perp_y),
                    (path_x[i] - perp_x, path_y[i] - perp_y),
                    (path_x[i+1] - perp_x, path_y[i+1] - perp_y),
                    (path_x[i+1] + perp_x, path_y[i+1] + perp_y)
                ]
                
                # Black stripes on top
                patch = Polygon(points, facecolor=black, edgecolor='none', alpha=1.0)
                ax.add_patch(patch)
    
    ax.axis('off')
    plt.tight_layout(pad=0)
    return fig

def main():
    """Generate all camouflage patterns"""
    print("=" * 60)
    print("CAMOUFLAGE PATTERN GENERATOR")
    print("=" * 60)
    
    # Ask user if they want to use an image
    use_image = input("\nDo you want to extract colors from an image? (y/n): ").lower().strip()
    
    colors = None
    if use_image == 'y':
        image_path = input("Enter the path to your image: ").strip()
        num_colors = input("How many colors to extract? (default: 4): ").strip()
        num_colors = int(num_colors) if num_colors else 4
        
        colors = extract_dominant_colors(image_path, num_colors)
        
        if colors is None:
            print("\nFalling back to default color palettes...")
            colors = None
    
    print("\n" + "=" * 60)
    print("Generating camouflage patterns...")
    print("=" * 60)
    
    # Generate woodland camo
    print("\n1. Woodland camouflage")
    fig1 = generate_woodland_camo(colors=colors)
    plt.savefig('woodland_camo.png', bbox_inches='tight', pad_inches=0, dpi=150)
    plt.close()
    print("   ✓ Saved: woodland_camo.png")
    
    # Generate digital camo
    print("\n2. Digital camouflage")
    fig2 = generate_digital_camo(colors=colors)
    plt.savefig('digital_camo.png', bbox_inches='tight', pad_inches=0, dpi=150)
    plt.close()
    print("   ✓ Saved: digital_camo.png")
    
    # Generate tiger stripe
    print("\n3. Tiger stripe camouflage")
    fig3 = generate_tiger_stripe(colors=colors)
    plt.savefig('tiger_stripe_camo.png', bbox_inches='tight', pad_inches=0, dpi=150)
    plt.close()
    print("   ✓ Saved: tiger_stripe_camo.png")
    
    print("\n" + "=" * 60)
    print("All patterns generated successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()