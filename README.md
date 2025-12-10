# Camouflage Shader Demo

This workspace contains a WebGL demo and a standalone GLSL fragment shader to generate natural-looking camouflage patterns for woodland, desert, and snowfield environments.

Files added:
- `index.html` — runnable WebGL demo (open in a browser).
- `shaders/camouflage.frag` — standalone GLSL ES 1.00 fragment shader for integration.

Usage:
- Open `index.html` in a modern browser (Chrome, Firefox, Edge). For local files, some browsers require serving via a local HTTP server. From PowerShell you can run:

```powershell
# from project root (D:\final code)
python -m http.server 8000; # then open http://localhost:8000/index.html
```

Controls in the demo:
- Mode: Woodland / Desert / Snow
- Scale: Pattern scale (small/large blobs)
- Contrast: Strength of tone separation
- Seed: Random seed for variation

How it works (high level):
- Uses fbm (fractal noise) to build large blobs, medium spots, and fine texture layers.
- Combines layers and maps values into 3-color palettes for each environment.
- Designed to be easy to port to engines supporting GLSL ES 1.00.

If you want, I can:
- Add a Python script to export textures at fixed resolutions.
- Produce variations (digital, brush-style, high-contrast) or add an additional arid-rock palette.
