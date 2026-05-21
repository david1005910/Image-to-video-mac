#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 Chrome Extension Video Generator for Google Colab
완전한 비디오 생성 코드 - Colab에서 바로 실행 가능
"""

# ============================================================================
# 1. 초기 설정 및 라이브러리 설치
# ============================================================================
print("="*60)
print("🎬 Chrome Extension Video Generator")
print("="*60)
print("\n📦 필수 라이브러리 설치 중...")

import subprocess
import sys

def install_packages():
    """필수 패키지 설치"""
    packages = [
        'moviepy',
        'pillow',
        'numpy',
        'opencv-python-headless',
        'imageio',
        'imageio-ffmpeg'
    ]
    
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package])
    
    # FFmpeg 설치
    subprocess.run(['apt-get', 'update'], capture_output=True)
    subprocess.run(['apt-get', 'install', '-y', 'ffmpeg'], capture_output=True)
    
    print("✅ 라이브러리 설치 완료")

# 설치 실행
install_packages()

# ============================================================================
# 2. 필요한 모듈 임포트
# ============================================================================
import os
import json
import base64
import glob
from io import BytesIO
from datetime import datetime
import numpy as np
from PIL import Image
import cv2

# MoviePy 임포트
from moviepy.editor import (
    ImageClip, VideoClip, CompositeVideoClip, 
    concatenate_videoclips, AudioClip, TextClip, vfx
)
from moviepy.audio.AudioClip import AudioClip

# Colab 전용 모듈
try:
    from google.colab import files
    from IPython.display import Video, display, HTML, clear_output
    IN_COLAB = True
except ImportError:
    IN_COLAB = False
    print("⚠️ Google Colab이 아닌 환경에서 실행 중")

# ============================================================================
# 3. 비디오 생성 클래스
# ============================================================================

class VideoGenerator:
    """Chrome Extension 이미지를 비디오로 변환"""
    
    def __init__(self, work_dir="/content/video_generation"):
        """초기화"""
        self.work_dir = work_dir
        self.session_id = None
        self.image_files = []
        self.video_config = {
            'duration_per_image': 3.0,
            'fps': 30,
            'resolution': (1920, 1080),
            'transition_type': 'crossfade',
            'transition_duration': 0.5,
            'enable_ken_burns': True,
            'zoom_ratio': 1.2,
            'color_filter': 'cinematic',
            'brightness': 1.0,
            'contrast': 1.1,
            'add_bgm': True,
            'quality': 'high'
        }
        self._setup_directories()
    
    def _setup_directories(self):
        """작업 디렉토리 설정"""
        os.makedirs(self.work_dir, exist_ok=True)
        os.makedirs(f"{self.work_dir}/images", exist_ok=True)
        os.makedirs(f"{self.work_dir}/output", exist_ok=True)
        print(f"📁 작업 디렉토리: {self.work_dir}")
    
    def load_json_data(self, json_path=None):
        """JSON 파일 로드 (Extension 데이터)"""
        if json_path and os.path.exists(json_path):
            with open(json_path, 'r') as f:
                data = json.load(f)
        elif IN_COLAB:
            print("\n📤 Chrome Extension JSON 파일을 업로드하세요:")
            uploaded = files.upload()
            if uploaded:
                json_path = list(uploaded.keys())[0]
                with open(json_path, 'r') as f:
                    data = json.load(f)
            else:
                raise ValueError("파일이 업로드되지 않았습니다")
        else:
            raise ValueError("JSON 파일 경로를 지정하세요")
        
        self.session_id = data.get('session_id', 'unknown')
        print(f"\n✅ 데이터 로드 완료")
        print(f"📌 Session ID: {self.session_id}")
        print(f"📸 이미지 수: {data.get('image_count', 0)}개")
        
        return data
    
    def process_images(self, images_data):
        """이미지 데이터 처리 및 저장"""
        print("\n🖼️ 이미지 처리 중...")
        self.image_files = []
        
        for idx, img_data in enumerate(images_data):
            try:
                # Data URL 처리
                if img_data['url'].startswith('data:'):
                    header, encoded = img_data['url'].split(',', 1)
                    img_bytes = base64.b64decode(encoded)
                    img = Image.open(BytesIO(img_bytes))
                    
                    # 이미지 저장
                    filename = img_data.get('filename', f'image_{idx:03d}.png')
                    img_path = f"{self.work_dir}/images/{filename}"
                    img.save(img_path)
                    self.image_files.append(img_path)
                    print(f"  ✓ {filename} ({img.size[0]}x{img.size[1]})")
                else:
                    print(f"  ⚠️ URL 이미지 건너뜀: {img_data['url'][:50]}...")
            except Exception as e:
                print(f"  ✗ 이미지 {idx} 처리 실패: {str(e)}")
        
        print(f"\n✅ 총 {len(self.image_files)}개 이미지 준비 완료")
        return self.image_files
    
    def create_ken_burns_effect(self, image_path, duration):
        """Ken Burns 효과 (줌/패닝) 생성"""
        clip = ImageClip(image_path, duration=duration)
        w, h = clip.size
        zoom_ratio = self.video_config['zoom_ratio']
        
        def make_frame(t):
            zoom = 1 + (zoom_ratio - 1) * (t / duration)
            new_w, new_h = int(w * zoom), int(h * zoom)
            x = (new_w - w) // 2
            y = (new_h - h) // 2
            
            frame = np.array(Image.open(image_path).resize((new_w, new_h)))
            return frame[y:y+h, x:x+w]
        
        return VideoClip(make_frame, duration=duration).set_fps(self.video_config['fps'])
    
    def apply_color_filter(self, clip):
        """색상 필터 적용"""
        filter_type = self.video_config['color_filter']
        
        if filter_type == 'cinematic':
            # 시네마틱: 대비 증가
            return clip.fx(vfx.colorx, 0.95).fx(vfx.lum_contrast, contrast=0.2)
        elif filter_type == 'vintage':
            # 빈티지: 따뜻한 톤
            return clip.fx(vfx.colorx, 1.1).fx(vfx.lum_contrast, contrast=-0.1)
        elif filter_type == 'cold':
            # 차가운 톤
            return clip.fx(vfx.colorx, 0.9)
        elif filter_type == 'warm':
            # 따뜻한 톤
            return clip.fx(vfx.colorx, 1.15)
        return clip
    
    def create_video(self):
        """메인 비디오 생성"""
        if not self.image_files:
            raise ValueError("이미지가 없습니다")
        
        print("\n🎬 비디오 생성 시작...")
        clips = []
        duration = self.video_config['duration_per_image']
        
        # 각 이미지를 클립으로 변환
        for idx, img_path in enumerate(self.image_files):
            print(f"처리 중: {idx+1}/{len(self.image_files)} - {os.path.basename(img_path)}")
            
            # Ken Burns 효과
            if self.video_config['enable_ken_burns']:
                try:
                    clip = self.create_ken_burns_effect(img_path, duration)
                except:
                    clip = ImageClip(img_path, duration=duration)
            else:
                clip = ImageClip(img_path, duration=duration)
            
            # 해상도 조정
            clip = clip.resize(self.video_config['resolution'])
            
            # 색상 필터
            if self.video_config['color_filter'] != 'none':
                clip = self.apply_color_filter(clip)
            
            # 밝기 조정
            if self.video_config['brightness'] != 1.0:
                clip = clip.fx(vfx.colorx, self.video_config['brightness'])
            
            clips.append(clip)
        
        # 클립 연결
        print("\n🔗 클립 연결 중...")
        if self.video_config['transition_type'] == 'crossfade' and len(clips) > 1:
            # 크로스페이드 전환
            trans_duration = self.video_config['transition_duration']
            final_clips = [clips[0]]
            
            for i in range(1, len(clips)):
                clips[i] = clips[i].crossfadein(trans_duration)
                clips[i] = clips[i].set_start(final_clips[-1].duration - trans_duration)
                final_clips.append(clips[i])
            
            video = CompositeVideoClip(final_clips)
        else:
            video = concatenate_videoclips(clips, method="compose")
        
        # BGM 추가
        if self.video_config['add_bgm']:
            print("🎵 BGM 추가 중...")
            video = self.add_background_music(video)
        
        print(f"✅ 비디오 생성 완료: {video.duration:.1f}초")
        return video
    
    def add_background_music(self, video):
        """배경 음악 추가"""
        def make_ambient(t):
            """앰비언트 사운드 생성"""
            frequencies = [110, 165, 220]  # A2, E3, A3
            signal = np.zeros_like(t)
            for freq in frequencies:
                signal += np.sin(2 * np.pi * freq * t) * 0.05
            return np.stack([signal, signal]).T if len(signal.shape) == 1 else signal
        
        audio = AudioClip(make_ambient, duration=video.duration)
        audio = audio.volumex(0.3)
        audio = audio.audio_fadein(2).audio_fadeout(2)
        
        return video.set_audio(audio)
    
    def render_video(self, video, output_name=None):
        """비디오 렌더링 및 저장"""
        if output_name is None:
            output_name = f"video_{self.session_id}.mp4"
        
        output_path = f"{self.work_dir}/output/{output_name}"
        
        # 품질 프리셋
        quality_presets = {
            'low': {'bitrate': '2M', 'crf': 28},
            'medium': {'bitrate': '5M', 'crf': 23},
            'high': {'bitrate': '10M', 'crf': 18},
            'ultra': {'bitrate': '20M', 'crf': 15}
        }
        
        quality = quality_presets[self.video_config['quality']]
        
        print(f"\n🎬 렌더링 시작...")
        print(f"📁 출력: {output_path}")
        print(f"🎯 품질: {self.video_config['quality']}")
        
        # 렌더링
        video.write_videofile(
            output_path,
            fps=self.video_config['fps'],
            codec='libx264',
            bitrate=quality['bitrate'],
            audio_codec='aac' if self.video_config['add_bgm'] else None,
            audio_bitrate='128k' if self.video_config['add_bgm'] else None,
            preset='medium',
            threads=4,
            verbose=False,
            logger=None
        )
        
        file_size = os.path.getsize(output_path) / (1024*1024)
        print(f"\n✅ 렌더링 완료!")
        print(f"📁 파일 크기: {file_size:.1f} MB")
        print(f"⏱️ 영상 길이: {video.duration:.1f}초")
        
        return output_path
    
    def run(self, json_path=None):
        """전체 프로세스 실행"""
        try:
            # 1. JSON 데이터 로드
            data = self.load_json_data(json_path)
            
            # 2. 이미지 처리
            self.process_images(data.get('images', []))
            
            # 3. 비디오 생성
            video = self.create_video()
            
            # 4. 렌더링
            output_path = self.render_video(video)
            
            # 5. 결과 표시 (Colab)
            if IN_COLAB:
                print("\n🎥 미리보기:")
                display(Video(output_path, embed=True, width=720))
                
                print("\n💾 다운로드:")
                files.download(output_path)
            
            return output_path
            
        except Exception as e:
            print(f"\n❌ 오류 발생: {str(e)}")
            raise

# ============================================================================
# 4. 간단한 실행 함수
# ============================================================================

def generate_video_simple(json_path=None, **kwargs):
    """간단한 비디오 생성 함수
    
    Args:
        json_path: Chrome Extension JSON 파일 경로
        **kwargs: 비디오 설정 (선택)
            - duration_per_image: 이미지당 표시 시간 (기본: 3초)
            - resolution: (width, height) 튜플 (기본: (1920, 1080))
            - transition_type: 'crossfade', 'none' (기본: 'crossfade')
            - enable_ken_burns: Ken Burns 효과 (기본: True)
            - color_filter: 'cinematic', 'vintage', 'cold', 'warm', 'none'
            - quality: 'low', 'medium', 'high', 'ultra' (기본: 'high')
    
    Returns:
        output_path: 생성된 비디오 파일 경로
    """
    generator = VideoGenerator()
    
    # 설정 업데이트
    for key, value in kwargs.items():
        if key in generator.video_config:
            generator.video_config[key] = value
    
    return generator.run(json_path)

# ============================================================================
# 5. 메인 실행 (Colab에서 실행)
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 비디오 생성을 시작하려면 아래 함수를 실행하세요:")
    print("="*60)
    print("""
# 기본 실행
output_path = generate_video_simple()

# 또는 커스텀 설정
output_path = generate_video_simple(
    duration_per_image=2.0,  # 이미지당 2초
    resolution=(1280, 720),   # HD 해상도
    transition_type='crossfade',
    enable_ken_burns=True,
    color_filter='cinematic',
    quality='high'
)
    """)
    
    # Colab에서 자동 실행
    if IN_COLAB:
        print("\n📌 자동으로 비디오 생성을 시작합니다...")
        try:
            output = generate_video_simple()
            print(f"\n🎉 비디오 생성 성공: {output}")
        except Exception as e:
            print(f"\n⚠️ 자동 실행 실패: {str(e)}")
            print("위의 generate_video_simple() 함수를 직접 실행하세요.")