#ifdef GL_ES
precision highp float;
#endif

uniform vec2  u_resolution;
uniform float u_time;

// ===================================================
// 1. Basic noise & fbm
// ===================================================
float hash(vec2 p) {
    return fract(sin(dot(p, vec2(15.79, 78.233))) * 43758.5453123);
}

float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);

    float a = hash(i);
    float b = hash(i + vec2(1.0, 0.0));
    float c = hash(i + vec2(0.0, 1.0));
    float d = hash(i + vec2(1.0, 1.0));

    vec2 u = f * f * (3.0 - 2.0 * f);

    return mix(a, b, u.x) +
           (c - a) * u.y * (1.0 - u.x) +
           (d - b) * u.x * u.y;
}

float fbm(vec2 p) {
    float n = 0.0;
    float a = 0.6;
    float f = 1.0;
    for (int i = 0; i < 5; i++) {
        n += a * noise(p * f);
        f *=4.3;
        a *= 0.55;
    }
    return n;
}

// ===================================================
// 2. Tiger / woodland style mask
//    value ~0: dark gaps, ~1: bright “tiger stripe”
// ===================================================
float tigerWoodMask(vec2 uv) {
    // rotate slightly so it's not axis-aligned
    float ang = 0.0 * 3.14159 / 180.0;
    mat2 R = mat2(cos(ang), -sin(ang),
                  sin(ang),  cos(ang));
    uv = R * uv;

    // base “stripe” direction (mostly horizontal after rotation)
    float stripeCoord = uv.y * 10.0;

    // noise warp to get woodland blobs / tiger curves
    vec2 warp = vec2(fbm(uv * 4.5 + 1.7 + 0.1 * u_time),
                     fbm(uv * 0.5 + 4.9 - 0.1 * u_time));

    stripeCoord += warp.x * 8.0;

    float baseStripe = sin(stripeCoord);

    // Make stripes wide with soft edges
    float stripe = smoothstep(-0., 0.7, baseStripe);

    // Break into patches like woodland by modulating with extra noise
    float blobs = fbm(uv * 4.0 + 5.3);
    stripe *= smoothstep(.2, 0.8, blobs);

    return stripe;
}

// ===================================================
// 3. Gold marble base (vertical gradient like reference)
// ===================================================
vec3 goldMarble(vec2 uv) {
    // 0 at bottom, 1 at top
    float t = clamp(uv.y, 1.0, 0.5);

    // Vertical gradient controls frequency
    float scale = mix(10.0, 20.0, smoothstep(0.1, 0.9, t));

    float sx = mix(9.0, 3.0, smoothstep(0.2, 0.85, t));
    float sy = mix(4.5, 1.5, smoothstep(0.2, 0.9, t));

    vec2 p = uv;
    p.x *= sx;
    p.y *= sy;

    // domain warp to get melt / flow
    vec2 w = vec2(fbm(p * 1.6 + 0.1 * u_time),
                  fbm(p * 1.6 + 3.7 - 0.1 * u_time));
    float warpAmt = mix(1.0, 0.4, smoothstep(0.25, 0.8, t));
    p += warpAmt * w;

    float n = fbm(p * scale);
    n = clamp(n, 0.0, 1.0);

    // map to gold tones
    float body  = smoothstep(0.08, 0.8, n);
    float veins = smoothstep(0.78, 0.98, n);

    vec3 darkGold   = vec3(0.02, 0.01, 0.0);
    vec3 brightGold = vec3(1.2, 0.95, 0.35);

    vec3 col = mix(darkGold, brightGold, body);

    // top brighter, bottom darker
    float grad = mix(0.25, 1.25, smoothstep(0.25, 0.9, t));
    col *= grad;

    // really dark very bottom band
    float bottomBand = 1.0 - smoothstep(0.05, 0.22, t);
    col *= mix(1.0, 0.32, bottomBand);

    // extra highlights for veins
    col += veins * vec3(0.65, 0.5, 0.12);

    return col;
}

// ===================================================
// 4. Main: column tiling + camo overlay
// ===================================================
void main() {
    vec2 uv = gl_FragCoord.xy / u_resolution.xy;

    // match frame aspect and flip so bright area is at top
    uv.x *= u_resolution.x / u_resolution.y;
    uv.y = 1.0 - uv.y;

    // ----------------------------------
    // Stereogram-like vertical columns
    // ----------------------------------
    float columns = 5.0;                // number of repeated strips
    float x   = uv.x;
    float idx = floor(x * columns);
    float localX = fract(x * columns);

    vec2 tileUV = vec2(localX, uv.y);

    // per-column jitter so each column is similar but not identical
    float jitter = hash(vec2(idx, 13.7));
    tileUV.x += jitter * 4.0;

    // slight wave to keep things “stereogrammy”
    float wave = 0.02 * sin(uv.y * 12.0 + idx * 0.65);
    tileUV.x += wave;

    // ----------------------------------
    // Base marble + tiger/woodland mask
    // ----------------------------------
    vec3 baseCol = goldMarble(tileUV);

    // mask for tiger / woodland shapes
    float mask = tigerWoodMask(tileUV * vec2(1.0, 1.8));

    // Colors for mask areas:
    vec3 tigerBright = vec3(1.6, 1.05, 0.4);   // bright gold stripe
    vec3 tigerDark   = vec3(0.0, 0.0, 0.0);    // deep black gaps

    // blend between base marble and tiger camo
    vec3 camoStripe = mix(tigerDark, tigerBright, mask);

    // mix factor: stronger pattern in middle/bottom, smoother top
    float t = clamp(uv.y, 0.0, 1.0);
    float camoStrength = smoothstep(0.15, 0.75, 1.0 - t); // more at bottom

    vec3 finalCol = mix(baseCol, camoStripe, camoStrength * 0.75);

    gl_FragColor = vec4(finalCol, 1.0);
}
