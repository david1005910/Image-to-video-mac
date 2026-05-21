#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size):
    """동영상 카메라 아이콘 생성"""
    # 배경 - 그라디언트 효과
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 배경 원 (그라디언트 효과를 위한 여러 원)
    center = size // 2
    for i in range(size//2, 0, -2):
        alpha = int(255 * (1 - i/(size/2)))
        color = (102, 126, 234, alpha)  # 보라색 그라디언트
        draw.ellipse([center-i, center-i, center+i, center+i], fill=color)
    
    # 메인 배경 원
    main_radius = int(size * 0.4)
    draw.ellipse(
        [center-main_radius, center-main_radius, 
         center+main_radius, center+main_radius],
        fill=(102, 126, 234, 255)  # 메인 보라색
    )
    
    # 카메라 본체
    cam_width = int(size * 0.5)
    cam_height = int(size * 0.35)
    cam_x = center - cam_width // 2
    cam_y = center - cam_height // 2
    
    # 카메라 본체 (흰색)
    draw.rounded_rectangle(
        [cam_x, cam_y, cam_x + cam_width, cam_y + cam_height],
        radius=size//20,
        fill='white'
    )
    
    # 카메라 렌즈
    lens_radius = int(size * 0.12)
    lens_x = cam_x + cam_width - lens_radius * 2 - size//20
    lens_y = center
    draw.ellipse(
        [lens_x - lens_radius, lens_y - lens_radius,
         lens_x + lens_radius, lens_y + lens_radius],
        fill=(50, 50, 50, 255)
    )
    
    # 렌즈 반사광
    reflect_radius = int(lens_radius * 0.3)
    draw.ellipse(
        [lens_x - reflect_radius, lens_y - reflect_radius,
         lens_x + reflect_radius, lens_y + reflect_radius],
        fill=(150, 150, 150, 255)
    )
    
    # 녹화 표시 (빨간 점)
    rec_radius = int(size * 0.05)
    rec_x = cam_x + size//10
    rec_y = cam_y + size//10
    draw.ellipse(
        [rec_x - rec_radius, rec_y - rec_radius,
         rec_x + rec_radius, rec_y + rec_radius],
        fill=(255, 0, 0, 255)
    )
    
    # 필름 스트립 효과 (선택적)
    if size >= 48:
        strip_height = int(size * 0.08)
        strip_y = cam_y + cam_height + size//20
        
        # 필름 스트립 배경
        draw.rectangle(
            [cam_x - size//10, strip_y, 
             cam_x + cam_width + size//10, strip_y + strip_height],
            fill=(30, 30, 30, 200)
        )
        
        # 필름 구멍들
        hole_size = int(strip_height * 0.4)
        hole_spacing = int(size * 0.1)
        for i in range(5):
            hole_x = cam_x - size//20 + i * hole_spacing
            draw.rectangle(
                [hole_x, strip_y + (strip_height - hole_size)//2,
                 hole_x + hole_size//2, strip_y + (strip_height + hole_size)//2],
                fill='white'
            )
    
    return img

# 각 크기별 아이콘 생성
sizes = {
    'icon-16.png': 16,
    'icon-48.png': 48,
    'icon-128.png': 128
}

for filename, size in sizes.items():
    icon = create_icon(size)
    icon.save(filename, 'PNG')
    print(f"Created {filename} ({size}x{size})")

print("✅ 모든 아이콘 생성 완료!")