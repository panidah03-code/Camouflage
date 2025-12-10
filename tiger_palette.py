# tiger_palette.py
# 1) Extract dominant colors from an Indochinese tiger photo
# 2) Save a palette image
# 3) Generate a Thai-style tiger stripe (shadow tiger) camouflage
#    using those colors

from PIL import Image, ImageDraw
import numpy as np
import random
import math


# --------------------------------------------------
# K-means for color clustering
# --------------------------------------------------
def kmeans(pixels, k=4, iters=20, seed=0):
    np.random.seed(seed)
    N = pixels.shape[0]
    centers = pixels[np.random.choice(N, k, replace=False)]
    for _ in range(iters):
        # assign
        dists = ((pixels[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
        labels = dists.argmin(axis=1)
        # update
        new_centers = []
        for i in range(k):
            if np.any(labels == i):
                new_centers.append(pixels[labels == i].mean(axis=0))
            else:
                new_centers.append(centers[i])
        centers = np.vstack(new_centers)
    return centers


def rgb_to_hex(rgb01):
    r, g, b = (np.clip(rgb01 * 255, 0, 255).astype(int))
    return "#{:02X}{:02X}{:02X}".format(r, g, b)


def save_palette_image(colors01, filename="tiger_palette.png",
                       swatch_w=80, h=200):
    """
    colors01: array of shape (k,3) in [0,1]
    Saves a vertical palette image: each color is a horizontal band.
    """
    k = len(colors01)
    img = Image.new("RGB", (swatch_w, h * k), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    for i, c in enumerate(colors01):
        r, g, b = (np.clip(c * 255, 0, 255).astype(int))
        y0 = i * h
        y1 = (i + 1) * h
        draw.rectangle([0, y0, swatch_w, y1], fill=(r, g, b))

    img.save(filename)
    print("Saved palette image to", filename)


# --------------------------------------------------
# Extract dominant tiger colors
# --------------------------------------------------
def extract_tiger_palette(path, k=4):
    img = Image.open(path).convert("RGB")

    # Crop to focus more on the tiger than the background
    w, h = img.size
    # You can adjust these numbers if you want more / less grass
    img = img.crop((int(w * 0.25), int(h * 0.2),
                    int(w * 0.95), int(h * 0.9)))

    img_small = img.resize((50, 50))
    arr = np.array(img_small, dtype=np.float32) / 255.0
    pixels = arr.reshape(-1, 3)

    centers = kmeans(pixels, k=k, iters=20, seed=0)

    # sort by brightness (dark → bright)
    lum = centers @ np.array([0.2126, 0.7152, 0.0722])
    order = np.argsort(lum)
    centers = centers[order]

    print("Dominant colors (dark → bright):")
    for c in centers:
        print(rgb_to_hex(c), c)

    # show them as an image
    save_palette_image(centers, "tiger_palette.png")

    return centers


# --------------------------------------------------
# Shadow tiger / Thai tiger stripe camouflage
# --------------------------------------------------
def make_tiger_stripe_camo(palette01, size=(512, 512),
                           stripe_scale=45,
                           filename="tiger_shadow_stripe_camo.png"):
    """
    palette01 : array (k,3) in [0,1] from extract_tiger_palette
    size      : (width, height) of output image
    stripe_scale : controls stripe thickness (bigger = thicker stripes)
    """
    w, h = size

    # convert colors to 0–255
    palette255 = [(int(c[0] * 255), int(c[1] * 255), int(c[2] * 255))
                  for c in palette01]

    # sort by brightness so 0 = darkest, -1 = lightest
    lum = [c[0] * 0.2126 + c[1] * 0.7152 + c[2] * 0.0722 for c in palette01]
    order = sorted(range(len(lum)), key=lambda i: lum[i])
    palette255 = [palette255[i] for i in order]

    dark = palette255[0]                          # dark stripe
    mid = palette255[1] if len(palette255) > 1 else palette255[0]
    light = palette255[2] if len(palette255) > 2 else palette255[-1]
    bg = palette255[-1]                           # lightest background

    # base image (background color)
    img_arr = np.zeros((h, w, 3), dtype=np.uint8)
    img_arr[:, :, :] = bg

    # stripe orientation (slightly diagonal)
    angle = math.radians(-20)
    cosA, sinA = math.cos(angle), math.sin(angle)

    phase = random.random() * 2 * math.pi

    for y in range(h):
        for x in range(w):
            # rotate coordinates so stripes run roughly diagonally
            u = x * cosA + y * sinA
            v = -x * sinA + y * cosA

            # sinusoidal base for stripes + small wobble by v
            s = math.sin(u / stripe_scale + phase +
                         0.4 * math.sin(v / 80.0))

            # small random jitter so edges aren’t perfect
            s += 0.3 * (random.random() - 0.5)

            if s > 0.6:
                color = dark          # main dark stripe
            elif s > 0.2:
                color = mid           # mid-tone band
            elif s > -0.1:
                color = light         # secondary lighter stripe
            else:
                color = bg            # background
            img_arr[y, x, :] = color

    img = Image.fromarray(img_arr, mode="RGB")
    img.save(filename)
    print("Saved tiger-stripe camo to", filename)


# --------------------------------------------------
# Main: run everything
# --------------------------------------------------
if __name__ == "__main__":
    # your tiger image path (inside the "images" folder)
    img_path = r"images\my_content.jpg"

    # 1) extract palette
    palette = extract_tiger_palette(img_path, k=4)

    # 2) generate Thai-style tiger stripe camo using that palette
    make_tiger_stripe_camo(palette,
                           size=(512, 512),
                           stripe_scale=45,
                           filename="tiger_shadow_stripe_camo.png")
