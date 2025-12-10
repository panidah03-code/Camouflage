// Standalone GLSL fragment shader (GLSL ES 1.00) for integration into engines
precision mediump float;
uniform vec2 u_res;
uniform float u_time;
uniform float u_scale;
uniform float u_contrast;
uniform float u_seed;
uniform int u_mode;
varying vec2 v_uv;

float hash(vec2 p){ p = fract(p * vec2(123.34, 456.21) + u_seed); p += dot(p, p + 45.32); return fract(p.x * p.y); }

float noise(vec2 p){ vec2 i = floor(p); vec2 f = fract(p); float a = hash(i + vec2(0.0,0.0)); float b = hash(i + vec2(1.0,0.0)); float c = hash(i + vec2(0.0,1.0)); float d = hash(i + vec2(1.0,1.0)); vec2 u = f*f*(3.0-2.0*f); return mix(a, b, u.x) + (c - a)*u.y*(1.0 - u.x) + (d - b)*u.x*u.y; }

float fbm(vec2 p){ float v=0.0; float a=0.5; mat2 m=mat2(1.6,1.2,-1.2,1.6); for(int i=0;i<5;i++){ v += a * noise(p); p = m*p*1.9; a *= 0.5; } return v; }

float blobs(vec2 p, float scale){ p *= scale; float b1 = fbm(p * 0.6 + 0.3*u_time); float b2 = fbm(p * 1.4 - 0.7*u_time); float spots = fbm(p * 3.0 + vec2(5.2)); float mixv = smoothstep(0.2, 0.8, mix(b1, b2, 0.5) * 0.8 + 0.2*spots); return mixv; }

vec3 palette(int mode, float t){ if(mode==0){ vec3 c0=vec3(0.08,0.18,0.05); vec3 c1=vec3(0.22,0.28,0.07); vec3 c2=vec3(0.36,0.22,0.08); return mix(mix(c0,c1, smoothstep(0.0,0.5,t)), c2, smoothstep(0.5,1.0,t)); } else if(mode==1){ vec3 c0=vec3(0.82,0.74,0.57); vec3 c1=vec3(0.66,0.55,0.38); vec3 c2=vec3(0.48,0.39,0.25); return mix(mix(c0,c1, smoothstep(0.0,0.5,t)), c2, smoothstep(0.5,1.0,t)); } else { vec3 c0=vec3(0.95,0.97,0.99); vec3 c1=vec3(0.85,0.88,0.92); vec3 c2=vec3(0.6,0.66,0.72); return mix(mix(c0,c1, smoothstep(0.0,0.5,t)), c2, smoothstep(0.5,1.0,t)); } }

void main(){ vec2 uv = v_uv * u_res / min(u_res.x, u_res.y); vec2 p = uv - 0.5 * u_res / min(u_res.x, u_res.y); float scale = u_scale; float large = blobs(p, scale * 0.6); float medium = blobs(p + 37.0, scale * 1.6); float fine = fbm(p * scale * 8.0 + 7.0); float t = mix(large, medium, 0.45); t = mix(t, fine * 0.7, 0.25); t = pow(t, 1.0 - 0.5 * u_contrast); float paletteIndex = clamp(t, 0.0, 1.0); vec3 color = palette(u_mode, paletteIndex); float light = 0.25 * fbm(p * scale * 0.7 + u_time * 0.05); color *= 0.9 + 0.15*light; if(u_mode==2){ color = mix(color, vec3(0.85,0.9,1.0), 0.07); } gl_FragColor = vec4(color,1.0); }
