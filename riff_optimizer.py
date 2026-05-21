#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 RIFF Format Optimizer & Advanced Codec Pipeline
RIFF/AVI 최적화 및 고급 코덱 지원
"""

import os
import subprocess
import logging
from pathlib import Path
import json
import time
from datetime import datetime

logger = logging.getLogger(__name__)

class RIFFOptimizer:
    """RIFF/AVI 포맷 최적화 클래스"""
    
    def __init__(self):
        self.supported_codecs = {
            'h264': {
                'codec': 'libx264',
                'container': 'mp4',
                'description': 'H.264 (가장 호환성 좋음)'
            },
            'h265': {
                'codec': 'libx265', 
                'container': 'mp4',
                'description': 'H.265 (더 작은 파일 크기)'
            },
            'av1': {
                'codec': 'libaom-av1',
                'container': 'mp4',
                'description': 'AV1 (최신 코덱, 최고 압축)'
            },
            'prores': {
                'codec': 'prores_ks',
                'container': 'mov',
                'description': 'ProRes (편집용 고품질)'
            },
            'dnxhd': {
                'codec': 'dnxhd',
                'container': 'mov', 
                'description': 'DNxHD (방송용 고품질)'
            },
            'riff_avi': {
                'codec': 'libx264',
                'container': 'avi',
                'description': 'RIFF/AVI (레거시 호환성)'
            }
        }
        
        self.quality_presets = {
            'draft': {'crf': 30, 'preset': 'ultrafast', 'bitrate': '2M'},
            'low': {'crf': 28, 'preset': 'fast', 'bitrate': '5M'},
            'medium': {'crf': 23, 'preset': 'medium', 'bitrate': '10M'},
            'high': {'crf': 18, 'preset': 'slow', 'bitrate': '20M'},
            'ultra': {'crf': 15, 'preset': 'veryslow', 'bitrate': '50M'},
            'lossless': {'crf': 0, 'preset': 'veryslow', 'bitrate': '100M'}
        }
    
    def check_ffmpeg_capabilities(self):
        """FFmpeg 기능 확인"""
        try:
            result = subprocess.run(
                ['ffmpeg', '-codecs'], 
                capture_output=True, text=True, check=True
            )
            
            available_codecs = []
            for codec_name, codec_info in self.supported_codecs.items():
                if codec_info['codec'] in result.stdout:
                    available_codecs.append(codec_name)
            
            logger.info(f"✅ 사용 가능한 코덱: {', '.join(available_codecs)}")
            return available_codecs
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ FFmpeg 확인 실패: {e}")
            return ['h264']  # 기본값
    
    def optimize_for_riff(self, input_path, output_path, quality='high'):
        """RIFF/AVI 포맷 최적화"""
        logger.info(f"🎯 RIFF/AVI 최적화: {input_path} → {output_path}")
        
        quality_settings = self.quality_presets[quality]
        
        cmd = [
            'ffmpeg', '-y',
            '-i', str(input_path),
            
            # RIFF/AVI 최적화 설정
            '-c:v', 'libx264',
            '-profile:v', 'high',
            '-level', '4.1',
            '-pix_fmt', 'yuv420p',
            
            # 품질 설정
            '-crf', str(quality_settings['crf']),
            '-preset', quality_settings['preset'],
            '-maxrate', quality_settings['bitrate'],
            '-bufsize', str(int(quality_settings['bitrate'].replace('M', '')) * 2) + 'M',
            
            # RIFF/AVI 특화 옵션
            '-vtag', 'H264',  # 비디오 태그
            '-f', 'avi',      # AVI 컨테이너 강제
            '-avoid_negative_ts', 'make_zero',
            
            str(output_path)
        ]
        
        return self._execute_ffmpeg_command(cmd, "RIFF/AVI 최적화")
    
    def create_multi_format_output(self, input_path, base_output_path, formats=None):
        """여러 포맷으로 동시 출력"""
        if formats is None:
            formats = ['h264', 'h265', 'riff_avi']
        
        logger.info(f"🎬 다중 포맷 출력: {', '.join(formats)}")
        
        results = {}
        base_path = Path(base_output_path)
        
        for format_name in formats:
            if format_name not in self.supported_codecs:
                logger.warning(f"지원하지 않는 포맷: {format_name}")
                continue
            
            codec_info = self.supported_codecs[format_name]
            output_path = base_path.with_suffix(f'_{format_name}.{codec_info["container"]}')
            
            success = self._convert_to_format(input_path, output_path, format_name)
            results[format_name] = {
                'success': success,
                'path': str(output_path) if success else None,
                'size_mb': output_path.stat().st_size / (1024*1024) if success and output_path.exists() else 0
            }
        
        return results
    
    def _convert_to_format(self, input_path, output_path, format_name):
        """특정 포맷으로 변환"""
        codec_info = self.supported_codecs[format_name]
        quality_settings = self.quality_presets['high']
        
        cmd = [
            'ffmpeg', '-y',
            '-i', str(input_path),
            '-c:v', codec_info['codec']
        ]
        
        # 코덱별 특화 설정
        if format_name == 'h264':
            cmd.extend([
                '-profile:v', 'high',
                '-preset', quality_settings['preset'],
                '-crf', str(quality_settings['crf'])
            ])
        elif format_name == 'h265':
            cmd.extend([
                '-preset', quality_settings['preset'],
                '-crf', str(quality_settings['crf']),
                '-tag:v', 'hvc1'
            ])
        elif format_name == 'av1':
            cmd.extend([
                '-cpu-used', '4',
                '-crf', str(quality_settings['crf']),
                '-b:v', '0'
            ])
        elif format_name == 'prores':
            cmd.extend([
                '-profile:v', '3',  # ProRes 422 HQ
                '-vendor', 'apl0'
            ])
        elif format_name == 'riff_avi':
            cmd.extend([
                '-profile:v', 'high',
                '-preset', quality_settings['preset'],
                '-crf', str(quality_settings['crf']),
                '-vtag', 'H264',
                '-f', 'avi'
            ])
        
        # 공통 설정
        cmd.extend([
            '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart' if codec_info['container'] == 'mp4' else '-movflags',
            str(output_path)
        ])
        
        # movflags 제거 (AVI용)
        if codec_info['container'] == 'avi':
            cmd = [arg for arg in cmd if not arg.startswith('-movflags') and arg != '+faststart']
        
        return self._execute_ffmpeg_command(cmd, f"{format_name.upper()} 변환")
    
    def optimize_for_streaming(self, input_path, output_path):
        """스트리밍 최적화"""
        logger.info(f"📡 스트리밍 최적화: {input_path} → {output_path}")
        
        cmd = [
            'ffmpeg', '-y',
            '-i', str(input_path),
            
            # 스트리밍 최적화 설정
            '-c:v', 'libx264',
            '-profile:v', 'baseline',  # 최대 호환성
            '-level', '3.1',
            '-preset', 'fast',
            '-crf', '23',
            
            # 스트리밍 특화
            '-maxrate', '5M',
            '-bufsize', '10M',
            '-g', '60',  # GOP 크기
            '-keyint_min', '60',
            '-sc_threshold', '0',
            
            # 픽셀 포맷 및 컨테이너
            '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart',
            '-f', 'mp4',
            
            str(output_path)
        ]
        
        return self._execute_ffmpeg_command(cmd, "스트리밍 최적화")
    
    def create_adaptive_bitrate_set(self, input_path, output_dir):
        """적응형 비트레이트 세트 생성 (HLS/DASH)"""
        logger.info(f"🌐 적응형 비트레이트 세트 생성")
        
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        # 다양한 해상도/비트레이트
        variants = [
            {'name': '240p', 'resolution': '426x240', 'bitrate': '400k'},
            {'name': '480p', 'resolution': '854x480', 'bitrate': '1000k'},
            {'name': '720p', 'resolution': '1280x720', 'bitrate': '2500k'},
            {'name': '1080p', 'resolution': '1920x1080', 'bitrate': '5000k'}
        ]
        
        results = {}
        
        for variant in variants:
            output_path = output_dir / f"{variant['name']}.mp4"
            
            cmd = [
                'ffmpeg', '-y',
                '-i', str(input_path),
                
                # 해상도 및 비트레이트 설정
                '-c:v', 'libx264',
                '-profile:v', 'high',
                '-preset', 'medium',
                '-b:v', variant['bitrate'],
                '-maxrate', variant['bitrate'],
                '-bufsize', str(int(variant['bitrate'].replace('k', '')) * 2) + 'k',
                '-vf', f"scale={variant['resolution']}",
                
                # 스트리밍 최적화
                '-g', '120',
                '-keyint_min', '120',
                '-sc_threshold', '0',
                '-pix_fmt', 'yuv420p',
                '-movflags', '+faststart',
                
                str(output_path)
            ]
            
            success = self._execute_ffmpeg_command(cmd, f"{variant['name']} 변환")
            results[variant['name']] = {
                'success': success,
                'path': str(output_path) if success else None
            }
        
        return results
    
    def _execute_ffmpeg_command(self, cmd, operation_name):
        """FFmpeg 명령어 실행"""
        try:
            logger.info(f"🔧 {operation_name} 실행 중...")
            
            start_time = time.time()
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=True,
                timeout=3600  # 1시간 타임아웃
            )
            
            elapsed_time = time.time() - start_time
            logger.info(f"✅ {operation_name} 완료 ({elapsed_time:.1f}초)")
            
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ {operation_name} 실패: {e}")
            logger.error(f"FFmpeg 오류: {e.stderr}")
            return False
        except subprocess.TimeoutExpired:
            logger.error(f"⏰ {operation_name} 시간 초과")
            return False
    
    def analyze_video_info(self, video_path):
        """비디오 정보 분석"""
        try:
            cmd = [
                'ffprobe', '-v', 'quiet',
                '-print_format', 'json',
                '-show_format', '-show_streams',
                str(video_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            info = json.loads(result.stdout)
            
            # 비디오 스트림 찾기
            video_stream = None
            for stream in info['streams']:
                if stream['codec_type'] == 'video':
                    video_stream = stream
                    break
            
            if video_stream:
                analysis = {
                    'duration': float(info['format']['duration']),
                    'size_mb': int(info['format']['size']) / (1024*1024),
                    'bitrate': int(info['format']['bit_rate']) if 'bit_rate' in info['format'] else 0,
                    'codec': video_stream['codec_name'],
                    'width': video_stream['width'],
                    'height': video_stream['height'],
                    'fps': eval(video_stream['r_frame_rate']),
                    'pixel_format': video_stream['pix_fmt']
                }
                
                logger.info(f"📊 비디오 분석 완료: {analysis['width']}x{analysis['height']} @ {analysis['fps']:.1f}fps")
                return analysis
            
        except Exception as e:
            logger.error(f"❌ 비디오 분석 실패: {e}")
        
        return None

class AdvancedVideoProcessor:
    """고급 비디오 처리 클래스"""
    
    def __init__(self, work_dir="./video_processing"):
        self.work_dir = Path(work_dir)
        self.work_dir.mkdir(exist_ok=True)
        
        self.riff_optimizer = RIFFOptimizer()
        self.processing_log = []
    
    def process_ai_video_with_riff_optimization(self, input_video_path, session_id):
        """AI 비디오를 RIFF 최적화 포함 다중 포맷으로 처리"""
        logger.info(f"🎬 고급 비디오 처리 시작: {input_video_path}")
        
        input_path = Path(input_video_path)
        if not input_path.exists():
            raise FileNotFoundError(f"입력 비디오를 찾을 수 없습니다: {input_path}")
        
        # 출력 디렉토리 설정
        output_dir = self.work_dir / session_id
        output_dir.mkdir(exist_ok=True)
        
        processing_start = time.time()
        
        # 1. 원본 분석
        logger.info("📊 원본 비디오 분석...")
        original_info = self.riff_optimizer.analyze_video_info(input_path)
        
        # 2. RIFF/AVI 최적화
        logger.info("🎯 RIFF/AVI 최적화...")
        riff_output = output_dir / f"{session_id}_optimized.avi"
        riff_success = self.riff_optimizer.optimize_for_riff(
            input_path, riff_output, quality='high'
        )
        
        # 3. 다중 포맷 출력
        logger.info("🎬 다중 포맷 생성...")
        multi_format_base = output_dir / f"{session_id}_multi"
        format_results = self.riff_optimizer.create_multi_format_output(
            input_path, multi_format_base,
            formats=['h264', 'h265', 'riff_avi']
        )
        
        # 4. 스트리밍 최적화
        logger.info("📡 스트리밍 최적화...")
        streaming_output = output_dir / f"{session_id}_streaming.mp4"
        streaming_success = self.riff_optimizer.optimize_for_streaming(
            input_path, streaming_output
        )
        
        # 5. 적응형 비트레이트 세트 (선택사항)
        logger.info("🌐 적응형 비트레이트 세트...")
        abr_dir = output_dir / "adaptive_bitrate"
        abr_results = self.riff_optimizer.create_adaptive_bitrate_set(
            input_path, abr_dir
        )
        
        # 6. 처리 결과 정리
        processing_time = time.time() - processing_start
        
        results = {
            'session_id': session_id,
            'processing_time': processing_time,
            'original_info': original_info,
            'outputs': {
                'riff_optimized': {
                    'success': riff_success,
                    'path': str(riff_output) if riff_success else None,
                    'size_mb': riff_output.stat().st_size / (1024*1024) if riff_success and riff_output.exists() else 0
                },
                'multi_format': format_results,
                'streaming_optimized': {
                    'success': streaming_success,
                    'path': str(streaming_output) if streaming_success else None,
                    'size_mb': streaming_output.stat().st_size / (1024*1024) if streaming_success and streaming_output.exists() else 0
                },
                'adaptive_bitrate': abr_results
            }
        }
        
        # 결과 저장
        results_file = output_dir / f"{session_id}_processing_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ 고급 비디오 처리 완료 ({processing_time:.1f}초)")
        self._print_processing_summary(results)
        
        return results
    
    def _print_processing_summary(self, results):
        """처리 결과 요약 출력"""
        print("\n" + "="*60)
        print("📊 고급 비디오 처리 결과 요약")
        print("="*60)
        
        if results['original_info']:
            info = results['original_info']
            print(f"🎬 원본: {info['width']}x{info['height']} @ {info['fps']:.1f}fps")
            print(f"📁 크기: {info['size_mb']:.1f} MB")
            print(f"⏱️ 길이: {info['duration']:.1f}초")
        
        print(f"🕐 처리 시간: {results['processing_time']:.1f}초")
        print()
        
        # RIFF 최적화 결과
        riff_result = results['outputs']['riff_optimized']
        status = "✅" if riff_result['success'] else "❌"
        print(f"{status} RIFF/AVI 최적화: {riff_result['size_mb']:.1f} MB")
        
        # 다중 포맷 결과
        print("🎬 다중 포맷 출력:")
        for format_name, format_result in results['outputs']['multi_format'].items():
            status = "✅" if format_result['success'] else "❌"
            print(f"  {status} {format_name.upper()}: {format_result['size_mb']:.1f} MB")
        
        # 스트리밍 최적화 결과
        streaming_result = results['outputs']['streaming_optimized']
        status = "✅" if streaming_result['success'] else "❌"
        print(f"{status} 스트리밍 최적화: {streaming_result['size_mb']:.1f} MB")
        
        # 적응형 비트레이트 결과
        print("🌐 적응형 비트레이트:")
        for variant_name, variant_result in results['outputs']['adaptive_bitrate'].items():
            status = "✅" if variant_result['success'] else "❌"
            print(f"  {status} {variant_name}")
        
        print("="*60)

def main():
    """메인 함수 - 고급 비디오 처리 테스트"""
    print("🎯 RIFF Optimizer & Advanced Video Processor")
    print("=" * 50)
    
    # 테스트용 입력
    input_video = input("📂 처리할 비디오 파일 경로: ").strip()
    if not os.path.exists(input_video):
        print(f"❌ 파일을 찾을 수 없습니다: {input_video}")
        return
    
    session_id = f"riff_test_{int(time.time())}"
    
    try:
        processor = AdvancedVideoProcessor()
        results = processor.process_ai_video_with_riff_optimization(
            input_video, session_id
        )
        
        print(f"\n🎉 처리 완료!")
        print(f"📁 결과 디렉토리: {processor.work_dir / session_id}")
        
    except Exception as e:
        print(f"\n❌ 처리 실패: {e}")

if __name__ == "__main__":
    main()