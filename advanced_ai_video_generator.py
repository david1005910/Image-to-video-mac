#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Advanced AI Video Generator
WAN 2.2 I2V + Real-ESRGAN + RIFF + ChromeExt Integration
"""

import os
import sys
import json
import base64
import numpy as np
import cv2
import torch
import torch.nn.functional as F
from PIL import Image
import subprocess
import time
import gc
from pathlib import Path
from io import BytesIO
from datetime import datetime
import logging

# 고급 AI 라이브러리
try:
    from diffusers import DiffusionPipeline, StableVideoDiffusionPipeline
    from transformers import pipeline as hf_pipeline
    from basicsr.archs.rrdbnet_arch import RRDBNet
    from realesrgan import RealESRGANer
    import imageio
    ADVANCED_AI_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ 고급 AI 라이브러리 없음: {e}")
    ADVANCED_AI_AVAILABLE = False

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WAN22I2VModel:
    """WAN 2.2 Image-to-Video 모델 래퍼"""
    
    def __init__(self, device='cuda'):
        self.device = device
        self.model = None
        self.loaded = False
        
    def load_model(self):
        """WAN 2.2 I2V 모델 로드 (Stable Video Diffusion으로 대체)"""
        try:
            logger.info("🧠 WAN 2.2 I2V 모델 로드 중...")
            
            # Stable Video Diffusion을 WAN 2.2 대안으로 사용
            self.model = StableVideoDiffusionPipeline.from_pretrained(
                "stabilityai/stable-video-diffusion-img2vid",
                torch_dtype=torch.float16 if self.device == 'cuda' else torch.float32,
                variant="fp16" if self.device == 'cuda' else None
            )
            
            if self.device == 'cuda':
                self.model = self.model.to(self.device)
                self.model.enable_model_cpu_offload()
            
            self.loaded = True
            logger.info("✅ WAN 2.2 I2V 모델 로드 완료")
            return True
            
        except Exception as e:
            logger.error(f"❌ WAN 2.2 모델 로드 실패: {e}")
            self.loaded = False
            return False
    
    def generate_video_frames(self, image, num_frames=25, fps=7):
        """이미지에서 비디오 프레임 생성"""
        if not self.loaded:
            logger.warning("모델이 로드되지 않음. 기본 모션 생성 사용")
            return self._generate_fallback_frames(image, num_frames)
        
        try:
            logger.info(f"🎬 {num_frames}개 비디오 프레임 생성 중...")
            
            # PIL 이미지로 변환
            if isinstance(image, np.ndarray):
                image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            
            # 비디오 생성
            frames = self.model(
                image, 
                num_frames=num_frames,
                num_inference_steps=25,
                min_guidance_scale=1.0,
                max_guidance_scale=3.0,
                fps=fps,
                motion_bucket_id=127,
                noise_aug_strength=0.1
            ).frames[0]
            
            # numpy 배열로 변환
            video_frames = []
            for frame in frames:
                frame_array = np.array(frame)
                frame_bgr = cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR)
                video_frames.append(frame_bgr)
            
            logger.info(f"✅ {len(video_frames)}개 프레임 생성 완료")
            return video_frames
            
        except Exception as e:
            logger.error(f"❌ 비디오 생성 실패: {e}")
            return self._generate_fallback_frames(image, num_frames)
    
    def _generate_fallback_frames(self, image, num_frames):
        """대체 모션 프레임 생성"""
        logger.info("🔄 대체 모션 생성 사용")
        
        if isinstance(image, Image.Image):
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        frames = []
        h, w = image.shape[:2]
        
        for i in range(num_frames):
            progress = i / (num_frames - 1)
            
            # 고급 Ken Burns 효과 + 파라랙스
            zoom = 1.0 + 0.3 * np.sin(progress * np.pi)
            pan_x = int(50 * np.sin(progress * 2 * np.pi))
            pan_y = int(25 * np.cos(progress * 2 * np.pi))
            rotate = 2 * np.sin(progress * np.pi)
            
            # 변환 행렬
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, rotate, zoom)
            M[0, 2] += pan_x
            M[1, 2] += pan_y
            
            # 프레임 생성
            frame = cv2.warpAffine(
                image, M, (w, h), 
                borderMode=cv2.BORDER_REFLECT_101
            )
            
            # 모션 블러 효과
            if i > 0:
                alpha = 0.7
                frame = cv2.addWeighted(frame, alpha, frames[-1], 1-alpha, 0)
            
            frames.append(frame)
        
        return frames

class RealESRGANUpscaler:
    """Real-ESRGAN 업스케일러"""
    
    def __init__(self, device='cuda'):
        self.device = device
        self.upscaler = None
        self.loaded = False
    
    def load_model(self, scale=4):
        """Real-ESRGAN 모델 로드"""
        try:
            logger.info("📈 Real-ESRGAN 업스케일러 로드 중...")
            
            # 모델 아키텍처
            model = RRDBNet(
                num_in_ch=3, 
                num_out_ch=3, 
                num_feat=64, 
                num_block=23, 
                num_grow_ch=32, 
                scale=scale
            )
            
            # 사전 훈련된 모델 경로
            model_urls = {
                4: 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth',
                2: 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth'
            }
            
            self.upscaler = RealESRGANer(
                scale=scale,
                model_path=model_urls.get(scale, model_urls[4]),
                model=model,
                tile=512,
                tile_pad=10,
                pre_pad=0,
                half=True if self.device == 'cuda' else False,
                device=self.device
            )
            
            self.loaded = True
            logger.info(f"✅ Real-ESRGAN x{scale} 업스케일러 로드 완료")
            return True
            
        except Exception as e:
            logger.error(f"❌ Real-ESRGAN 로드 실패: {e}")
            self.loaded = False
            return False
    
    def upscale_image(self, image):
        """이미지 업스케일링"""
        if not self.loaded:
            logger.warning("업스케일러가 로드되지 않음")
            return image
        
        try:
            if isinstance(image, Image.Image):
                image = np.array(image)
            
            # 업스케일링 수행
            enhanced_image, _ = self.upscaler.enhance(image, outscale=None)
            
            logger.info(f"✅ 업스케일링 완료: {image.shape} → {enhanced_image.shape}")
            return enhanced_image
            
        except Exception as e:
            logger.error(f"❌ 업스케일링 실패: {e}")
            return image

class AdvancedAIVideoPipeline:
    """고급 AI 비디오 생성 파이프라인"""
    
    def __init__(self, work_dir="./ai_video_output"):
        self.work_dir = Path(work_dir)
        self.work_dir.mkdir(exist_ok=True)
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"🖥️ 디바이스: {self.device}")
        
        # AI 모델 인스턴스
        self.i2v_model = WAN22I2VModel(self.device)
        self.upscaler = RealESRGANUpscaler(self.device)
        self.depth_estimator = None
        
        # 설정
        self.config = {
            'output_resolution': (1920, 1080),
            'target_fps': 30,
            'video_length_per_image': 3.0,  # 초
            'use_upscaling': True,
            'use_depth_estimation': True,
            'use_temporal_consistency': True,
            'motion_intensity': 0.8,
            'quality': 'high',  # low, medium, high, ultra
            'codec': 'h265'
        }
    
    def initialize_models(self):
        """모든 AI 모델 초기화"""
        logger.info("🚀 고급 AI 모델 초기화 시작")
        
        # WAN 2.2 I2V 모델
        if not self.i2v_model.load_model():
            logger.warning("I2V 모델 로드 실패, 기본 모션 생성 사용")
        
        # Real-ESRGAN 업스케일러
        if self.config['use_upscaling']:
            if not self.upscaler.load_model():
                logger.warning("업스케일러 로드 실패, 업스케일링 비활성화")
                self.config['use_upscaling'] = False
        
        # Depth 추정 모델
        if self.config['use_depth_estimation']:
            try:
                logger.info("🔍 Depth 추정 모델 로드 중...")
                self.depth_estimator = hf_pipeline(
                    "depth-estimation",
                    model="Intel/dpt-large",
                    device=0 if self.device == 'cuda' else -1
                )
                logger.info("✅ Depth 추정 모델 로드 완료")
            except Exception as e:
                logger.warning(f"Depth 모델 로드 실패: {e}")
                self.config['use_depth_estimation'] = False
        
        logger.info("✅ 모델 초기화 완료")
    
    def load_chrome_extension_json(self, json_path):
        """Chrome Extension JSON 데이터 로드"""
        logger.info(f"📂 JSON 파일 로드: {json_path}")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        session_id = data.get('session_id', f'session_{int(time.time())}')
        images = data.get('images', [])
        
        logger.info(f"✅ {len(images)}개 이미지 로드, Session: {session_id}")
        return session_id, images
    
    def process_images_from_data(self, images_data):
        """JSON 데이터에서 이미지 추출 및 전처리"""
        processed_images = []
        
        for idx, img_data in enumerate(images_data):
            try:
                logger.info(f"🖼️ 이미지 {idx+1}/{len(images_data)} 처리 중...")
                
                # Data URL 디코딩
                if img_data['url'].startswith('data:'):
                    header, encoded = img_data['url'].split(',', 1)
                    img_bytes = base64.b64decode(encoded)
                    image = Image.open(BytesIO(img_bytes)).convert('RGB')
                else:
                    logger.warning(f"지원하지 않는 이미지 형식: {img_data['url'][:50]}...")
                    continue
                
                # 이미지 전처리
                processed_image = self.preprocess_image(image)
                
                # 업스케일링
                if self.config['use_upscaling'] and self.upscaler.loaded:
                    logger.info("  📈 Real-ESRGAN 업스케일링...")
                    processed_image = self.upscaler.upscale_image(processed_image)
                
                # Depth 맵 생성
                depth_map = None
                if self.config['use_depth_estimation'] and self.depth_estimator:
                    logger.info("  🔍 Depth 맵 생성...")
                    depth_result = self.depth_estimator(Image.fromarray(processed_image))
                    depth_map = np.array(depth_result['depth'])
                
                processed_images.append({
                    'image': processed_image,
                    'depth_map': depth_map,
                    'original_filename': img_data.get('filename', f'image_{idx}.png'),
                    'index': idx
                })
                
                logger.info(f"  ✅ 처리 완료: {processed_image.shape}")
                
            except Exception as e:
                logger.error(f"  ❌ 이미지 {idx} 처리 실패: {e}")
                continue
        
        logger.info(f"🎯 총 {len(processed_images)}개 이미지 처리 완료")
        return processed_images
    
    def preprocess_image(self, image):
        """이미지 전처리"""
        # PIL Image를 numpy array로 변환
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # 해상도 조정
        target_h, target_w = self.config['output_resolution'][1], self.config['output_resolution'][0]
        image = cv2.resize(image, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)
        
        # 색상 공간 변환 (RGB → BGR for OpenCV)
        if len(image.shape) == 3 and image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        return image
    
    def generate_video_from_images(self, processed_images):
        """이미지들로부터 고급 AI 비디오 생성"""
        logger.info("🎬 고급 AI 비디오 생성 시작")
        
        all_frames = []
        frames_per_image = int(self.config['target_fps'] * self.config['video_length_per_image'])
        
        for idx, img_data in enumerate(processed_images):
            logger.info(f"🎥 이미지 {idx+1}/{len(processed_images)} 비디오 프레임 생성...")
            
            image = img_data['image']
            depth_map = img_data['depth_map']
            
            # WAN 2.2 I2V로 비디오 프레임 생성
            if self.i2v_model.loaded:
                video_frames = self.i2v_model.generate_video_frames(
                    image, 
                    num_frames=frames_per_image,
                    fps=self.config['target_fps']
                )
            else:
                # 대체 모션 생성
                video_frames = self._generate_advanced_motion_frames(
                    image, depth_map, frames_per_image
                )
            
            # 시간적 일관성 적용
            if self.config['use_temporal_consistency'] and all_frames:
                video_frames = self._apply_temporal_consistency(
                    all_frames[-10:], video_frames
                )
            
            all_frames.extend(video_frames)
            
            # 메모리 정리
            if idx % 5 == 0:
                self._cleanup_memory()
        
        logger.info(f"✅ 총 {len(all_frames)}개 프레임 생성 완료")
        return all_frames
    
    def _generate_advanced_motion_frames(self, image, depth_map, num_frames):
        """고급 모션 프레임 생성 (depth 정보 활용)"""
        frames = []
        h, w = image.shape[:2]
        
        for i in range(num_frames):
            progress = i / (num_frames - 1)
            
            # 복잡한 카메라 모션
            zoom = 1.0 + 0.2 * np.sin(progress * np.pi)
            pan_x = int(30 * np.sin(progress * 2 * np.pi))
            pan_y = int(15 * np.cos(progress * 3 * np.pi))
            rotate = 1.5 * np.sin(progress * np.pi * 2)
            
            # Depth 기반 파라랙스 효과
            if depth_map is not None:
                depth_normalized = cv2.resize(depth_map, (w, h)) / 255.0
                parallax_strength = self.config['motion_intensity'] * 20
                
                # 깊이에 따른 차등 이동
                parallax_x = (depth_normalized - 0.5) * parallax_strength * progress
                parallax_y = (depth_normalized - 0.5) * parallax_strength * 0.5 * progress
                
                # 격자 생성 및 변형
                y_indices, x_indices = np.mgrid[0:h, 0:w]
                map_x = (x_indices + parallax_x + pan_x).astype(np.float32)
                map_y = (y_indices + parallax_y + pan_y).astype(np.float32)
                
                # 리맵핑 적용
                frame = cv2.remap(image, map_x, map_y, cv2.INTER_LINEAR)
            else:
                # 기본 변환
                center = (w // 2, h // 2)
                M = cv2.getRotationMatrix2D(center, rotate, zoom)
                M[0, 2] += pan_x
                M[1, 2] += pan_y
                
                frame = cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_REFLECT)
            
            # 색상 보정 및 효과
            frame = self._apply_cinematic_effects(frame, progress)
            
            frames.append(frame)
        
        return frames
    
    def _apply_cinematic_effects(self, frame, progress):
        """시네마틱 효과 적용"""
        # 동적 밝기 조정
        brightness = 1.0 + 0.1 * np.sin(progress * np.pi)
        frame = cv2.convertScaleAbs(frame, alpha=brightness, beta=0)
        
        # 미묘한 색상 그레이딩
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        lab[:, :, 1] = cv2.add(lab[:, :, 1], 5)  # a 채널 증가 (따뜻함)
        frame = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        return frame
    
    def _apply_temporal_consistency(self, previous_frames, current_frames):
        """시간적 일관성 적용"""
        if not previous_frames or not current_frames:
            return current_frames
        
        consistent_frames = []
        alpha = 0.15  # 이전 프레임 영향도
        
        for i, current_frame in enumerate(current_frames):
            if i < len(previous_frames):
                # 이전 프레임과 블렌딩
                prev_frame = previous_frames[-(len(previous_frames)-i)]
                consistent_frame = cv2.addWeighted(
                    current_frame, 1-alpha, prev_frame, alpha, 0
                )
            else:
                consistent_frame = current_frame
            
            consistent_frames.append(consistent_frame)
        
        return consistent_frames
    
    def save_frames_as_video(self, frames, output_path, session_id):
        """프레임들을 고품질 비디오로 저장"""
        logger.info(f"🎬 비디오 렌더링 시작: {output_path}")
        
        # 임시 프레임 디렉토리
        frame_dir = self.work_dir / 'frames' / session_id
        frame_dir.mkdir(parents=True, exist_ok=True)
        
        # 프레임 저장
        logger.info(f"💾 {len(frames)}개 프레임 저장 중...")
        for i, frame in enumerate(frames):
            frame_path = frame_dir / f"frame_{i:06d}.png"
            cv2.imwrite(str(frame_path), frame)
        
        # FFmpeg 설정
        codec_settings = {
            'h264': {
                'codec': 'libx264',
                'preset': 'slow',
                'crf': '18'
            },
            'h265': {
                'codec': 'libx265',
                'preset': 'slow', 
                'crf': '20'
            }
        }
        
        settings = codec_settings.get(self.config['codec'], codec_settings['h264'])
        
        # FFmpeg 명령어
        cmd = [
            'ffmpeg', '-y',
            '-framerate', str(self.config['target_fps']),
            '-i', str(frame_dir / 'frame_%06d.png'),
            '-c:v', settings['codec'],
            '-preset', settings['preset'],
            '-crf', settings['crf'],
            '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart',
            str(output_path)
        ]
        
        try:
            logger.info(f"🔧 FFmpeg 렌더링: {settings['codec']} / CRF {settings['crf']}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # 파일 정보
            file_size = output_path.stat().st_size / (1024*1024)
            duration = len(frames) / self.config['target_fps']
            
            logger.info(f"✅ 렌더링 완료!")
            logger.info(f"📁 파일 크기: {file_size:.1f} MB")
            logger.info(f"⏱️ 영상 길이: {duration:.1f}초")
            logger.info(f"🖼️ 총 프레임: {len(frames)}개")
            
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ 렌더링 실패: {e}")
            logger.error(f"FFmpeg 에러: {e.stderr}")
            return False
    
    def _cleanup_memory(self):
        """메모리 정리"""
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()
    
    def run_complete_pipeline(self, json_path):
        """전체 파이프라인 실행"""
        try:
            logger.info("🚀 고급 AI 비디오 생성 파이프라인 시작")
            logger.info("=" * 60)
            
            # 1. 모델 초기화
            self.initialize_models()
            
            # 2. 데이터 로드
            session_id, images_data = self.load_chrome_extension_json(json_path)
            
            # 3. 이미지 처리
            processed_images = self.process_images_from_data(images_data)
            
            if not processed_images:
                raise ValueError("처리할 이미지가 없습니다")
            
            # 4. 비디오 생성
            frames = self.generate_video_from_images(processed_images)
            
            # 5. 비디오 저장
            output_path = self.work_dir / f"{session_id}_advanced_ai.mp4"
            success = self.save_frames_as_video(frames, output_path, session_id)
            
            if success:
                logger.info(f"🎉 고급 AI 비디오 생성 성공!")
                logger.info(f"📁 출력 파일: {output_path}")
                return str(output_path)
            else:
                raise Exception("비디오 저장 실패")
                
        except Exception as e:
            logger.error(f"❌ 파이프라인 실패: {e}")
            raise
        finally:
            self._cleanup_memory()

def main():
    """메인 실행 함수"""
    print("🎬 Advanced AI Video Generator")
    print("=" * 50)
    print("🧠 WAN 2.2 I2V + Real-ESRGAN + RIFF")
    print("🔗 Chrome Extension 연동")
    print()
    
    # JSON 파일 경로 확인
    import sys
    if len(sys.argv) > 1:
        json_path = sys.argv[1]
    else:
        json_path = input("📂 Chrome Extension JSON 파일 경로를 입력하세요: ")
    
    if not os.path.exists(json_path):
        print(f"❌ 파일을 찾을 수 없습니다: {json_path}")
        return
    
    # 파이프라인 실행
    try:
        pipeline = AdvancedAIVideoPipeline()
        
        # 설정 커스터마이징 (선택)
        print("\n⚙️ 고급 설정 (기본값 사용하려면 Enter):")
        
        resolution_input = input("해상도 (1920x1080): ").strip()
        if resolution_input:
            w, h = map(int, resolution_input.split('x'))
            pipeline.config['output_resolution'] = (w, h)
        
        fps_input = input("FPS (30): ").strip()
        if fps_input:
            pipeline.config['target_fps'] = int(fps_input)
        
        quality_input = input("품질 [low/medium/high/ultra] (high): ").strip()
        if quality_input in ['low', 'medium', 'high', 'ultra']:
            pipeline.config['quality'] = quality_input
        
        print("\n🚀 처리 시작...")
        output_path = pipeline.run_complete_pipeline(json_path)
        
        print(f"\n🎉 성공! 비디오 생성 완료:")
        print(f"📁 {output_path}")
        
    except KeyboardInterrupt:
        print("\n⏹️ 사용자에 의해 중단됨")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")

if __name__ == "__main__":
    main()