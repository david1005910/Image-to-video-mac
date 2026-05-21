#!/usr/bin/env python3
"""
🎬 Basic Video Generation Test (FFmpeg Only)
기본 비디오 생성 테스트 (의존성 최소화)
"""

import json
import base64
import subprocess
import os
import tempfile
from pathlib import Path
import time

def decode_image_from_json(json_path):
    """JSON에서 이미지 추출 및 저장"""
    print(f"📂 JSON 파일 로드: {json_path}")
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    session_id = data.get('session_id', 'test')
    images = data.get('images', [])
    
    print(f"🆔 Session ID: {session_id}")
    print(f"🖼️ 이미지 수: {len(images)}")
    
    # 임시 디렉토리 생성
    temp_dir = Path(tempfile.mkdtemp())
    image_files = []
    
    for i, img_data in enumerate(images):
        if img_data['url'].startswith('data:'):
            # Data URL에서 이미지 데이터 추출
            header, encoded = img_data['url'].split(',', 1)
            img_bytes = base64.b64decode(encoded)
            
            # 이미지 파일 저장
            img_path = temp_dir / f"image_{i:03d}.png"
            with open(img_path, 'wb') as f:
                f.write(img_bytes)
            
            image_files.append(str(img_path))
            print(f"  ✅ 이미지 {i+1} 저장: {img_path}")
    
    return session_id, image_files, temp_dir

def create_video_with_ffmpeg(image_files, output_path, duration_per_image=3, fps=30):
    """FFmpeg로 이미지들을 비디오로 변환"""
    print(f"\n🎬 FFmpeg 비디오 생성 시작...")
    print(f"📹 출력: {output_path}")
    print(f"⏱️ 이미지당 {duration_per_image}초, {fps}fps")
    
    if not image_files:
        raise ValueError("이미지 파일이 없습니다")
    
    # 각 이미지를 지정된 시간만큼 반복하여 프레임 생성
    total_frames = len(image_files) * duration_per_image * fps
    
    # 임시 프레임 디렉토리 생성
    frame_dir = Path(tempfile.mkdtemp())
    
    frame_count = 0
    for img_idx, img_file in enumerate(image_files):
        frames_for_this_image = duration_per_image * fps
        
        print(f"  🖼️ 이미지 {img_idx+1}/{len(image_files)} 처리 중...")
        
        for frame_idx in range(frames_for_this_image):
            frame_path = frame_dir / f"frame_{frame_count:06d}.png"
            
            # 간단한 복사 (실제로는 크기 조정이나 효과를 추가할 수 있음)
            subprocess.run([
                'cp', str(img_file), str(frame_path)
            ], check=True)
            
            frame_count += 1
    
    print(f"  📊 총 {frame_count}개 프레임 생성")
    
    # FFmpeg로 비디오 생성
    cmd = [
        'ffmpeg', '-y',
        '-framerate', str(fps),
        '-i', str(frame_dir / 'frame_%06d.png'),
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-pix_fmt', 'yuv420p',
        '-movflags', '+faststart',
        str(output_path)
    ]
    
    print(f"  🔧 FFmpeg 명령어 실행...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # 결과 정보
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / (1024*1024)
            duration = frame_count / fps
            
            print(f"  ✅ 비디오 생성 성공!")
            print(f"  📁 파일 크기: {file_size:.1f} MB")
            print(f"  ⏱️ 영상 길이: {duration:.1f}초")
            print(f"  🎯 품질: H.264, {fps}fps")
            
            return True
        else:
            print(f"  ❌ 출력 파일이 생성되지 않음")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"  ❌ FFmpeg 실행 실패: {e}")
        print(f"  오류 출력: {e.stderr}")
        return False
    finally:
        # 임시 파일 정리
        import shutil
        shutil.rmtree(frame_dir, ignore_errors=True)

def test_basic_video_generation():
    """기본 비디오 생성 테스트"""
    print("🧪 Basic Video Generation Test")
    print("=" * 50)
    
    # 1. 테스트 JSON 파일 확인
    json_path = "test_enhanced.json"
    if not os.path.exists(json_path):
        # 향상된 테스트 파일이 없으면 기본 테스트 파일 시도
        json_path = "test_simple.json"
        if not os.path.exists(json_path):
            print(f"❌ 테스트 JSON 파일이 없습니다: {json_path}")
            print("먼저 create_test_image.py를 실행하여 테스트 데이터를 생성하세요.")
            return False
    
    try:
        # 2. JSON에서 이미지 추출
        session_id, image_files, temp_dir = decode_image_from_json(json_path)
        
        # 3. 비디오 생성
        output_path = f"{session_id}_basic_test.mp4"
        success = create_video_with_ffmpeg(
            image_files, 
            output_path, 
            duration_per_image=2,  # 2초씩
            fps=15  # 15fps로 낮게
        )
        
        # 4. 임시 파일 정리
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        if success:
            print(f"\n🎉 기본 비디오 생성 테스트 성공!")
            print(f"📁 출력 파일: {output_path}")
            print(f"▶️ 재생 명령어: open {output_path}")
            
            # 파일 정보 표시
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / (1024*1024)
                print(f"📊 최종 파일 크기: {file_size:.2f} MB")
            
            return True
        else:
            print(f"\n❌ 비디오 생성 실패")
            return False
            
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        return False

def test_ffmpeg_capabilities():
    """FFmpeg 기능 상세 테스트"""
    print("\n🔍 FFmpeg 상세 기능 테스트")
    print("-" * 30)
    
    # 사용 가능한 코덱 확인
    try:
        result = subprocess.run(['ffmpeg', '-encoders'], capture_output=True, text=True)
        output = result.stdout
        
        codecs_to_check = ['libx264', 'libx265', 'libaom-av1']
        available_codecs = []
        
        for codec in codecs_to_check:
            if codec in output:
                available_codecs.append(codec)
                print(f"  ✅ {codec} 사용 가능")
            else:
                print(f"  ❌ {codec} 없음")
        
        return available_codecs
        
    except Exception as e:
        print(f"  ❌ 코덱 확인 실패: {e}")
        return ['libx264']  # 기본값

if __name__ == "__main__":
    # FFmpeg 기능 확인
    available_codecs = test_ffmpeg_capabilities()
    
    # 기본 비디오 생성 테스트
    success = test_basic_video_generation()
    
    if success:
        print("\n" + "=" * 50)
        print("🎯 테스트 결과 요약")
        print("=" * 50)
        print("✅ JSON 파싱 및 이미지 추출: 성공")
        print("✅ Base64 디코딩: 성공") 
        print("✅ FFmpeg 비디오 생성: 성공")
        print(f"🎬 사용 가능한 코덱: {', '.join(available_codecs)}")
        print("\n🚀 기본 비디오 파이프라인이 정상 작동합니다!")
        print("💡 고급 AI 기능을 원한다면 Python 패키지를 설치하세요:")
        print("   pip install pillow numpy opencv-python torch")
    else:
        print("\n❌ 기본 테스트 실패")
        print("FFmpeg 설치 및 설정을 확인하세요.")