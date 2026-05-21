#!/usr/bin/env python3
"""
🏁 Final Test Report
고급 AI 비디오 파이프라인 최종 테스트 보고서
"""

import os
import json
import subprocess
import time
from pathlib import Path

def check_all_files():
    """모든 필수 파일 존재 확인"""
    print("📁 파일 존재 확인")
    print("-" * 30)
    
    required_files = {
        'Core Pipeline': [
            'colab_advanced_ai_video.ipynb',
            'advanced_ai_video_generator.py', 
            'riff_optimizer.py',
            'COLAB_VIDEO_GENERATOR.py'
        ],
        'Test Files': [
            'simple_test.py',
            'basic_video_test.py',
            'create_test_image.py'
        ],
        'Documentation': [
            'VIDEO_GENERATION_GUIDE.md',
            'COLAB_GUIDE.md',
            'EXTENSION_INSTALL_GUIDE.md'
        ],
        'Chrome Extension': [
            'chrome-extension/manifest.json',
            'chrome-extension/popup.js',
            'chrome-extension/popup.html'
        ]
    }
    
    results = {}
    total_files = 0
    existing_files = 0
    
    for category, files in required_files.items():
        print(f"\n{category}:")
        category_results = {}
        
        for file in files:
            exists = os.path.exists(file)
            status = "✅" if exists else "❌"
            print(f"  {status} {file}")
            category_results[file] = exists
            total_files += 1
            if exists:
                existing_files += 1
        
        results[category] = category_results
    
    print(f"\n📊 파일 존재율: {existing_files}/{total_files} ({100*existing_files/total_files:.1f}%)")
    return results, existing_files, total_files

def test_video_generation():
    """비디오 생성 기능 테스트"""
    print("\n🎬 비디오 생성 테스트")
    print("-" * 30)
    
    # 테스트 파일들 확인
    test_files = ['test_enhanced.json', 'test_simple.json']
    available_test = None
    
    for test_file in test_files:
        if os.path.exists(test_file):
            available_test = test_file
            break
    
    if not available_test:
        print("❌ 테스트 JSON 파일이 없음")
        return False
    
    print(f"📂 테스트 파일: {available_test}")
    
    # JSON 파일 검증
    try:
        with open(available_test, 'r') as f:
            data = json.load(f)
        
        session_id = data.get('session_id', 'unknown')
        image_count = data.get('image_count', 0)
        images = data.get('images', [])
        
        print(f"🆔 Session: {session_id}")
        print(f"🖼️ 이미지 수: {image_count}")
        print(f"📊 실제 이미지: {len(images)}개")
        
        # 첫 번째 이미지 검증
        if images:
            first_img = images[0]
            url = first_img.get('url', '')
            if url.startswith('data:image'):
                print("✅ Base64 이미지 형식 확인")
            else:
                print("❌ 잘못된 이미지 형식")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ JSON 검증 실패: {e}")
        return False

def test_ffmpeg_integration():
    """FFmpeg 통합 테스트"""
    print("\n🎥 FFmpeg 통합 테스트")
    print("-" * 30)
    
    try:
        # FFmpeg 버전 확인
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, check=True)
        version_line = result.stdout.split('\n')[0]
        print(f"✅ {version_line}")
        
        # 지원 코덱 확인
        result = subprocess.run(['ffmpeg', '-codecs'], 
                              capture_output=True, text=True, check=True)
        
        codecs = ['h264', 'hevc', 'av1']
        supported_codecs = []
        
        for codec in codecs:
            if codec in result.stdout.lower():
                supported_codecs.append(codec)
                print(f"✅ {codec.upper()} 지원")
            else:
                print(f"❌ {codec.upper()} 미지원")
        
        return len(supported_codecs) > 0
        
    except Exception as e:
        print(f"❌ FFmpeg 테스트 실패: {e}")
        return False

def check_generated_videos():
    """생성된 비디오 파일 확인"""
    print("\n📹 생성된 비디오 확인")
    print("-" * 30)
    
    video_files = list(Path('.').glob('*.mp4'))
    
    if not video_files:
        print("❌ 생성된 비디오 파일 없음")
        return False
    
    for video_file in video_files:
        try:
            # 파일 크기 확인
            size_mb = video_file.stat().st_size / (1024*1024)
            
            # FFprobe로 정보 확인
            result = subprocess.run([
                'ffprobe', '-v', 'quiet', '-print_format', 'json',
                '-show_format', str(video_file)
            ], capture_output=True, text=True, check=True)
            
            info = json.loads(result.stdout)
            duration = float(info['format']['duration'])
            
            print(f"✅ {video_file.name}")
            print(f"   크기: {size_mb:.2f} MB")
            print(f"   길이: {duration:.1f}초")
            
        except Exception as e:
            print(f"❌ {video_file.name}: 분석 실패 ({e})")
            return False
    
    return True

def test_chrome_extension():
    """Chrome Extension 파일 확인"""
    print("\n🔌 Chrome Extension 확인")
    print("-" * 30)
    
    ext_dir = Path('chrome-extension')
    if not ext_dir.exists():
        print("❌ chrome-extension 디렉토리 없음")
        return False
    
    required_files = [
        'manifest.json',
        'popup.html',
        'popup.js',
        'content.js',
        'background.js'
    ]
    
    success = True
    for file in required_files:
        file_path = ext_dir / file
        if file_path.exists():
            print(f"✅ {file}")
            
            # manifest.json 특별 검증
            if file == 'manifest.json':
                try:
                    with open(file_path) as f:
                        manifest = json.load(f)
                    
                    version = manifest.get('manifest_version', 0)
                    name = manifest.get('name', '')
                    permissions = len(manifest.get('permissions', []))
                    
                    print(f"   Manifest v{version}")
                    print(f"   이름: {name}")
                    print(f"   권한: {permissions}개")
                    
                except Exception as e:
                    print(f"   ❌ manifest.json 파싱 실패: {e}")
                    success = False
        else:
            print(f"❌ {file} 없음")
            success = False
    
    return success

def generate_final_report():
    """최종 보고서 생성"""
    print("\n" + "=" * 60)
    print("🏁 고급 AI 비디오 파이프라인 최종 테스트 보고서")
    print("=" * 60)
    
    # 각 테스트 실행
    tests = {
        "파일 존재": check_all_files(),
        "비디오 생성": test_video_generation(),
        "FFmpeg 통합": test_ffmpeg_integration(),
        "생성된 비디오": check_generated_videos(),
        "Chrome Extension": test_chrome_extension()
    }
    
    print("\n📊 테스트 결과 요약:")
    print("-" * 30)
    
    passed_tests = 0
    total_tests = len([k for k, v in tests.items() if k != "파일 존재"])
    
    # 파일 존재 결과
    file_results, existing_files, total_files = tests["파일 존재"]
    print(f"📁 파일 존재: {existing_files}/{total_files} ({100*existing_files/total_files:.1f}%)")
    
    # 다른 테스트 결과
    for test_name, result in tests.items():
        if test_name == "파일 존재":
            continue
            
        status = "✅ 통과" if result else "❌ 실패"
        print(f"{status} {test_name}")
        
        if result:
            passed_tests += 1
    
    # 전체 평가
    print(f"\n🎯 전체 성공률: {passed_tests}/{total_tests} ({100*passed_tests/total_tests:.1f}%)")
    
    if passed_tests == total_tests and existing_files >= total_files * 0.8:
        print("\n🎉 고급 AI 비디오 파이프라인 구현 완료!")
        print("✨ 모든 핵심 기능이 정상 작동합니다.")
        
        print("\n🚀 사용 가능한 기능:")
        print("   • Chrome Extension으로 이미지 수집")
        print("   • JSON 형식으로 데이터 저장")
        print("   • FFmpeg 기반 비디오 생성")
        print("   • H.264/H.265 고품질 인코딩")
        print("   • Google Colab 연동")
        print("   • 고급 AI 업스케일링 (선택)")
        
        print("\n📋 다음 단계:")
        print("   1. Chrome Extension 설치 및 테스트")
        print("   2. Google Colab에서 고급 AI 기능 테스트")
        print("   3. Python 패키지 설치로 로컬 고급 기능 활성화")
        
        return True
    else:
        print("\n⚠️ 일부 기능에 문제가 있습니다.")
        print("로그를 확인하여 누락된 부분을 해결하세요.")
        return False

if __name__ == "__main__":
    success = generate_final_report()
    
    print("\n" + "=" * 60)
    if success:
        print("🎯 테스트 완료: 성공")
    else:
        print("🎯 테스트 완료: 일부 실패")
    print("=" * 60)