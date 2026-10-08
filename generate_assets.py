import os
import math
import json
import struct
from PIL import Image, ImageDraw, ImageFilter, ImageFont

os.makedirs("assets/frames", exist_ok=True)

# Brand Colors
COLOR_BONE = (229, 215, 196)      # #E5D7C4
COLOR_TAN = (207, 187, 153)       # #CFBB99
COLOR_MOSS = (136, 144, 99)       # #889063
COLOR_KOMBU = (53, 64, 36)        # #354024
COLOR_CAFE = (76, 61, 25)         # #4C3D19
COLOR_DARK_BG = (28, 24, 18)      # Dark warm background

def create_hero_bg():
    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), COLOR_DARK_BG)
    draw = ImageDraw.Draw(img)

    # Ambient luxury gradient lighting
    for r in range(800, 0, -20):
        alpha = int(255 * (1 - r / 800) * 0.4)
        color = (
            int(COLOR_CAFE[0] + (COLOR_TAN[0] - COLOR_CAFE[0]) * (1 - r/800)),
            int(COLOR_CAFE[1] + (COLOR_TAN[1] - COLOR_CAFE[1]) * (1 - r/800)),
            int(COLOR_CAFE[2] + (COLOR_TAN[2] - COLOR_CAFE[2]) * (1 - r/800))
        )
        draw.ellipse([width//2 - r, height//2 - r, width//2 + r, height//2 + r], fill=color)

    # Add subtle geometric arabesque decorative motifs
    for i in range(0, width, 120):
        for j in range(0, height, 120):
            draw.rectangle([i+30, j+30, i+90, j+90], outline=(COLOR_TAN[0], COLOR_TAN[1], COLOR_TAN[2], 20), width=1)
            draw.ellipse([i+40, j+40, i+80, j+80], outline=(COLOR_MOSS[0], COLOR_MOSS[1], COLOR_MOSS[2], 15), width=1)

    # Blur layer heavily for luxury ambient hero background
    img = img.filter(ImageFilter.GaussianBlur(radius=35))

    # Add warm vignette
    vignette = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(vignette)
    vdraw.rectangle([0, 0, width, height], fill=(15, 12, 10, 160))
    vdraw.ellipse([200, 100, width - 200, height - 100], fill=(0, 0, 0, 0))
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=80))

    img = Image.alpha_composite(img.convert("RGBA"), vignette).convert("RGB")
    img.save("assets/hero-bg.jpg", quality=92)
    print("Created assets/hero-bg.jpg")

def create_product_images():
    products = [
        ("Damascus Sovereign Sofa", "أريكة السيادة الدمشقية", "assets/product-1.jpg", COLOR_KOMBU, COLOR_TAN),
        ("Al-Shahba Royal Console", "كونسول الشهباء الملكي", "assets/product-2.jpg", COLOR_CAFE, COLOR_BONE),
        ("Silk Walnut Dining Set", "طاولة طعام الجوز والحرير", "assets/product-3.jpg", COLOR_MOSS, COLOR_CAFE),
        ("Imperial Velvet Armchair", "كرسي فاخر مخملي", "assets/product-4.jpg", COLOR_TAN, COLOR_KOMBU),
    ]

    for title_en, title_ar, filepath, bg_color, accent_color in products:
        width, height = 800, 600
        img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(img)

        # Draw luxury podium and background geometry
        draw.ellipse([100, 380, 700, 560], fill=(int(bg_color[0]*0.7), int(bg_color[1]*0.7), int(bg_color[2]*0.7)))
        draw.ellipse([150, 410, 650, 530], fill=accent_color)

        # Abstract furniture silhouette
        draw.rounded_rectangle([250, 200, 550, 420], radius=30, fill=(int(accent_color[0]*0.85), int(accent_color[1]*0.85), int(accent_color[2]*0.85)), outline=COLOR_BONE, width=3)
        draw.rounded_rectangle([280, 160, 520, 280], radius=20, fill=accent_color, outline=COLOR_BONE, width=2)
        draw.rounded_rectangle([230, 260, 280, 400], radius=15, fill=COLOR_CAFE)
        draw.rounded_rectangle([520, 260, 570, 400], radius=15, fill=COLOR_CAFE)

        # Draw legs
        draw.polygon([(270, 420), (280, 420), (275, 480), (265, 480)], fill=COLOR_CAFE)
        draw.polygon([(520, 420), (530, 420), (535, 480), (525, 480)], fill=COLOR_CAFE)

        # Lighting gradient overlay
        overlay = Image.new("RGBA", (width, height), (0,0,0,0))
        odraw = ImageDraw.Draw(overlay)
        odraw.ellipse([200, -50, 600, 350], fill=(255, 255, 255, 30))
        overlay = overlay.filter(ImageFilter.GaussianBlur(radius=40))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

        # Label badge
        badge = Image.new("RGBA", (width, 80), (0, 0, 0, 120))
        img.paste(badge, (0, height - 80), badge)

        img.save(filepath, quality=90)
        print(f"Created {filepath}")

def create_frames():
    num_frames = 60
    width, height = 1280, 720

    for f in range(1, num_frames + 1):
        angle = (f / num_frames) * 2 * math.pi
        img = Image.new("RGB", (width, height), (22, 20, 18))
        draw = ImageDraw.Draw(img)

        # Soft backdrop studio spotlight
        for r in range(400, 0, -25):
            intensity = int(180 * (1 - r / 400))
            draw.ellipse([width//2 - r, height//2 - 50 - r, width//2 + r, height//2 - 50 + r],
                         fill=(intensity//2 + 30, intensity//2 + 25, intensity//3 + 20))

        # Pedestal shadow
        draw.ellipse([width//2 - 250, height//2 + 150, width//2 + 250, height//2 + 230], fill=(10, 8, 6))

        # Rotating 3D furniture model projection simulation
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        center_x, center_y = width // 2, height // 2 + 20

        # Base seat
        seat_w = 220
        seat_d = 180 * abs(cos_a) + 120
        seat_h = 50

        x1 = center_x - seat_w * 0.5 * cos_a - seat_d * 0.3 * sin_a
        y1 = center_y + seat_w * 0.2 * sin_a - seat_d * 0.1 * cos_a
        x2 = center_x + seat_w * 0.5 * cos_a - seat_d * 0.3 * sin_a
        y2 = center_y - seat_w * 0.2 * sin_a - seat_d * 0.1 * cos_a
        x3 = center_x + seat_w * 0.5 * cos_a + seat_d * 0.3 * sin_a
        y3 = center_y - seat_w * 0.2 * sin_a + seat_d * 0.1 * cos_a
        x4 = center_x - seat_w * 0.5 * cos_a + seat_d * 0.3 * sin_a
        y4 = center_y + seat_w * 0.2 * sin_a + seat_d * 0.1 * cos_a

        # Cushion top polygon
        draw.polygon([(x1, y1 - seat_h), (x2, y2 - seat_h), (x3, y3 - seat_h), (x4, y4 - seat_h)], fill=COLOR_TAN, outline=COLOR_BONE)
        # Seat front face
        draw.polygon([(x3, y3 - seat_h), (x4, y4 - seat_h), (x4, y4), (x3, y3)], fill=COLOR_CAFE, outline=COLOR_KOMBU)
        draw.polygon([(x4, y4 - seat_h), (x1, y1 - seat_h), (x1, y1), (x4, y4)], fill=COLOR_KOMBU, outline=COLOR_CAFE)

        # Backrest curve
        back_h = 160
        draw.polygon([(x1, y1 - seat_h), (x2, y2 - seat_h), (x2, y2 - seat_h - back_h), (x1, y1 - seat_h - back_h)], fill=COLOR_MOSS, outline=COLOR_BONE)

        # Armrests
        arm_h = 90
        draw.rectangle([x4 - 30, y4 - seat_h - arm_h, x4 + 10, y4 - seat_h], fill=COLOR_TAN, outline=COLOR_CAFE)
        draw.rectangle([x3 - 10, y3 - seat_h - arm_h, x3 + 30, y3 - seat_h], fill=COLOR_TAN, outline=COLOR_CAFE)

        # Legs
        leg_len = 100
        for lx, ly in [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]:
            draw.line([(lx, ly), (lx + 10 * sin_a, ly + leg_len)], fill=COLOR_CAFE, width=8)
            draw.line([(lx, ly), (lx + 10 * sin_a, ly + leg_len)], fill=COLOR_TAN, width=4)

        # Frame counter & Brand overlay tag
        draw.text((40, height - 50), f"AL-SHAHBA 360° FRAME {f:03d}/060", fill=COLOR_TAN)
        draw.text((width - 240, 40), "مفروشات الشهباء - العرض التفاعلي", fill=COLOR_BONE)

        fname = f"assets/frames/frame_{f:03d}.jpg"
        img.save(fname, quality=88)

    print("Created 60 canvas frames in assets/frames/")

def create_glb_model():
    """Generates a valid GLB 2.0 3D model of a luxury armchair."""

    # We build mesh boxes for backrest, seat cushion, left armrest, right armrest, and 4 legs.
    boxes = []

    def add_box(center, size, color_rgb):
        cx, cy, cz = center
        sx, sy, sz = [s * 0.5 for s in size]
        r, g, b = [c / 255.0 for c in color_rgb]

        # 8 vertices
        local_verts = [
            [cx - sx, cy - sy, cz - sz], # 0
            [cx + sx, cy - sy, cz - sz], # 1
            [cx + sx, cy + sy, cz - sz], # 2
            [cx - sx, cy + sy, cz - sz], # 3
            [cx - sx, cy - sy, cz + sz], # 4
            [cx + sx, cy - sy, cz + sz], # 5
            [cx + sx, cy + sy, cz + sz], # 6
            [cx - sx, cy + sy, cz + sz], # 7
        ]

        # 6 faces * 2 triangles = 12 triangles
        faces = [
            # Front
            (4, 5, 6, 0, 0, 1), (4, 6, 7, 0, 0, 1),
            # Back
            (1, 0, 3, 0, 0, -1), (1, 3, 2, 0, 0, -1),
            # Top
            (7, 6, 2, 0, 1, 0), (7, 2, 3, 0, 1, 0),
            # Bottom
            (0, 1, 5, 0, -1, 0), (0, 5, 4, 0, -1, 0),
            # Right
            (5, 1, 2, 1, 0, 0), (5, 2, 6, 1, 0, 0),
            # Left
            (0, 4, 7, -1, 0, 0), (0, 7, 3, -1, 0, 0),
        ]

        return local_verts, faces, (r, g, b, 1.0)

    # Armchair parts:
    # Seat cushion (Tan)
    parts = [
        # Seat
        ([0, 0.4, 0], [0.8, 0.15, 0.8], COLOR_TAN),
        # Backrest
        ([0, 0.85, -0.35], [0.8, 0.75, 0.15], COLOR_KOMBU),
        # Left Armrest
        ([-0.42, 0.55, 0], [0.12, 0.35, 0.85], COLOR_MOSS),
        # Right Armrest
        ([0.42, 0.55, 0], [0.12, 0.35, 0.85], COLOR_MOSS),
        # Legs (Café Noir)
        ([-0.35, 0.16, -0.35], [0.08, 0.32, 0.08], COLOR_CAFE),
        ([0.35, 0.16, -0.35], [0.08, 0.32, 0.08], COLOR_CAFE),
        ([-0.35, 0.16, 0.35], [0.08, 0.32, 0.08], COLOR_CAFE),
        ([0.35, 0.16, 0.35], [0.08, 0.32, 0.08], COLOR_CAFE),
    ]

    positions = []
    normals = []
    colors = []
    indices = []

    vert_offset = 0
    for center, size, color in parts:
        verts, faces, color_rgba = add_box(center, size, color)
        for v in verts:
            positions.extend(v)
            colors.extend(color_rgba)
            normals.extend([0.0, 1.0, 0.0]) # basic normal

        for f in faces:
            indices.extend([vert_offset + f[0], vert_offset + f[1], vert_offset + f[2]])
        vert_offset += len(verts)

    # Convert lists to binary data
    pos_bin = struct.pack(f'<{len(positions)}f', *positions)
    norm_bin = struct.pack(f'<{len(normals)}f', *normals)
    col_bin = struct.pack(f'<{len(colors)}f', *colors)
    idx_bin = struct.pack(f'<{len(indices)}H', *indices)

    # Padding buffers to 4-byte alignment
    def pad4(data):
        rem = len(data) % 4
        if rem > 0:
            data += b'\x00' * (4 - rem)
        return data

    pos_bin = pad4(pos_bin)
    norm_bin = pad4(norm_bin)
    col_bin = pad4(col_bin)
    idx_bin = pad4(idx_bin)

    buffer_data = idx_bin + pos_bin + norm_bin + col_bin

    # Calculate min/max for POSITION
    min_x = min(positions[0::3])
    max_x = max(positions[0::3])
    min_y = min(positions[1::3])
    max_y = max(positions[1::3])
    min_z = min(positions[2::3])
    max_z = max(positions[2::3])

    buffer_views = [
        {"buffer": 0, "byteOffset": 0, "byteLength": len(idx_bin), "target": 34963}, # ELEMENT_ARRAY_BUFFER
        {"buffer": 0, "byteOffset": len(idx_bin), "byteLength": len(pos_bin), "target": 34962}, # ARRAY_BUFFER
        {"buffer": 0, "byteOffset": len(idx_bin) + len(pos_bin), "byteLength": len(norm_bin), "target": 34962},
        {"buffer": 0, "byteOffset": len(idx_bin) + len(pos_bin) + len(norm_bin), "byteLength": len(col_bin), "target": 34962},
    ]

    accessors = [
        {"bufferView": 0, "byteOffset": 0, "componentType": 5123, "count": len(indices), "type": "SCALAR"}, # UNSIGNED_SHORT
        {"bufferView": 1, "byteOffset": 0, "componentType": 5126, "count": len(positions) // 3, "type": "VEC3", "min": [min_x, min_y, min_z], "max": [max_x, max_y, max_z]}, # FLOAT
        {"bufferView": 2, "byteOffset": 0, "componentType": 5126, "count": len(normals) // 3, "type": "VEC3"},
        {"bufferView": 3, "byteOffset": 0, "componentType": 5126, "count": len(colors) // 4, "type": "VEC4"},
    ]

    gltf_json = {
        "asset": {"version": "2.0", "generator": "Al-Shahba Custom Asset Generator"},
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "name": "AlShahbaLuxuryArmchair"}],
        "meshes": [
            {
                "name": "LuxuryArmchairMesh",
                "primitives": [
                    {
                        "attributes": {
                            "POSITION": 1,
                            "NORMAL": 2,
                            "COLOR_0": 3
                        },
                        "indices": 0
                    }
                ]
            }
        ],
        "buffers": [{"byteLength": len(buffer_data)}],
        "bufferViews": buffer_views,
        "accessors": accessors
    }

    json_str = json.dumps(gltf_json, separators=(',', ':')).encode('utf-8')
    while len(json_str) % 4 != 0:
        json_str += b' '

    json_chunk_len = len(json_str)
    bin_chunk_len = len(buffer_data)

    total_len = 12 + 8 + json_chunk_len + 8 + bin_chunk_len

    # GLB Header
    header = struct.pack('<4sII', b'glTF', 2, total_len)

    # JSON Chunk Header
    json_chunk_hdr = struct.pack('<II', json_chunk_len, 0x4E4F534A) # JSON

    # BIN Chunk Header
    bin_chunk_hdr = struct.pack('<II', bin_chunk_len, 0x04576162) # BIN

    glb_content = header + json_chunk_hdr + json_str + bin_chunk_hdr + buffer_data

    with open("assets/chair_fast.glb", "wb") as f:
        f.write(glb_content)

    print("Created valid assets/chair_fast.glb model!")

if __name__ == "__main__":
    create_hero_bg()
    create_product_images()
    create_frames()
    create_glb_model()
