#!/usr/bin/env python3
"""
🎨 Test Image Creator
FFmpeg 호환 테스트 이미지 생성
"""

import base64
import json
import time

def create_valid_png_image():
    """유효한 PNG 이미지 생성 (256x256 컬러)"""
    
    # 256x256 빨간색 PNG 이미지 데이터
    # PNG 헤더 + 적절한 IDAT 청크 + IEND
    width, height = 256, 256
    
    # PNG 시그니처
    png_signature = b'\x89PNG\r\n\x1a\n'
    
    # IHDR 청크 (256x256, 8비트 트루컬러)
    ihdr_data = width.to_bytes(4, 'big') + height.to_bytes(4, 'big') + b'\x08\x02\x00\x00\x00'
    ihdr_crc = 0x9A20A6E4  # 미리 계산된 CRC
    ihdr_chunk = b'IHDR' + ihdr_data + ihdr_crc.to_bytes(4, 'big')
    ihdr = len(ihdr_data).to_bytes(4, 'big') + ihdr_chunk
    
    # 간단한 빨간색 픽셀 데이터 생성 (압축되지 않은 형태)
    # 각 행: 필터 바이트(0) + RGB 데이터
    row_data = b'\x00' + (b'\xFF\x00\x00' * width)  # 빨간색 픽셀들
    image_data = row_data * height
    
    # zlib 압축 (간단한 deflate)
    import zlib
    compressed_data = zlib.compress(image_data)
    
    # IDAT 청크
    idat_chunk = b'IDAT' + compressed_data
    idat_crc = zlib.crc32(idat_chunk) & 0xffffffff
    idat = len(compressed_data).to_bytes(4, 'big') + idat_chunk + idat_crc.to_bytes(4, 'big')
    
    # IEND 청크
    iend = b'\x00\x00\x00\x00IEND\xaeB`\x82'
    
    # PNG 파일 조합
    png_data = png_signature + ihdr + idat + iend
    
    return png_data

def create_gradient_test_images(count=3):
    """그라디언트 테스트 이미지들 생성"""
    images = []
    
    for i in range(count):
        # 간단히 각각 다른 색상의 PNG 생성
        # 여기서는 ImageMagick convert 명령어를 사용
        import subprocess
        import tempfile
        import os
        
        # 임시 파일 생성
        temp_file = f"/tmp/test_image_{i}.png"
        
        # 다른 색상 생성
        colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
        color = colors[i % len(colors)]
        
        # ImageMagick으로 단색 이미지 생성
        try:
            subprocess.run([
                'convert', '-size', '256x256', f'xc:{color}', temp_file
            ], check=True, capture_output=True)
            
            # PNG 파일 읽기
            with open(temp_file, 'rb') as f:
                png_data = f.read()
            
            # 정리
            os.remove(temp_file)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            # ImageMagick이 없는 경우, Python으로 간단한 PNG 생성
            print(f"ImageMagick 없음, 기본 PNG 사용")
            png_data = create_simple_color_png(256, 256, i)
        
        # Base64 인코딩
        data_url = f"data:image/png;base64,{base64.b64encode(png_data).decode()}"
        
        images.append({
            "url": data_url,
            "filename": f"test_image_{i+1:02d}.png",
            "timestamp": int(time.time()) + i,
            "type": "generated",
            "color": color
        })
        
        print(f"✅ 테스트 이미지 {i+1} 생성: {color} ({len(png_data)} bytes)")
    
    return images

def create_simple_color_png(width, height, color_index):
    """간단한 컬러 PNG 생성 (ImageMagick 없을 때)"""
    # RGB 색상 정의
    colors = [
        (255, 0, 0),    # 빨강
        (0, 255, 0),    # 초록  
        (0, 0, 255),    # 파랑
        (255, 255, 0),  # 노랑
        (255, 0, 255),  # 자주
        (0, 255, 255),  # 청록
    ]
    
    r, g, b = colors[color_index % len(colors)]
    
    # PNG 헤더
    png_signature = b'\x89PNG\r\n\x1a\n'
    
    # IHDR 청크 생성
    def create_ihdr(w, h):
        data = w.to_bytes(4, 'big') + h.to_bytes(4, 'big')
        data += b'\x08\x02\x00\x00\x00'  # 8비트, 트루컬러
        
        import zlib
        crc = zlib.crc32(b'IHDR' + data) & 0xffffffff
        return len(data).to_bytes(4, 'big') + b'IHDR' + data + crc.to_bytes(4, 'big')
    
    # 이미지 데이터 생성
    row_data = b'\x00' + bytes([r, g, b] * width)
    image_data = row_data * height
    
    # 압축
    import zlib
    compressed = zlib.compress(image_data)
    
    # IDAT 청크
    def create_idat(data):
        crc = zlib.crc32(b'IDAT' + data) & 0xffffffff
        return len(data).to_bytes(4, 'big') + b'IDAT' + data + crc.to_bytes(4, 'big')
    
    # IEND 청크
    iend = b'\x00\x00\x00\x00IEND\xaeB`\x82'
    
    return png_signature + create_ihdr(width, height) + create_idat(compressed) + iend

def create_enhanced_test_json():
    """개선된 테스트 JSON 생성"""
    print("🎨 향상된 테스트 이미지 생성 중...")
    
    # 테스트 이미지들 생성
    images = create_gradient_test_images(3)
    
    # Chrome Extension 형식 JSON
    test_data = {
        "session_id": f"enhanced_test_{int(time.time())}",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "image_count": len(images),
        "images": images
    }
    
    # JSON 파일 저장
    output_file = "test_enhanced.json"
    with open(output_file, "w") as f:
        json.dump(test_data, f, indent=2)
    
    print(f"✅ 향상된 테스트 JSON 생성: {output_file}")
    print(f"📊 이미지 수: {len(images)}")
    
    return output_file

if __name__ == "__main__":
    create_enhanced_test_json()