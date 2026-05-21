#!/usr/bin/env python3
"""
🧪 Simple Test for Advanced AI Video Pipeline
고급 AI 비디오 파이프라인 간단 테스트
"""

import json
import base64
import time
import os
import subprocess

def test_modules_import():
    """모듈 임포트 테스트"""
    print("🔍 모듈 임포트 테스트")
    print("-" * 30)
    
    results = {}
    
    # 기본 Python 모듈들
    basic_modules = ['json', 'base64', 'time', 'os', 'subprocess']
    for module in basic_modules:
        try:
            __import__(module)
            results[module] = True
        except ImportError:
            results[module] = False
    
    print(f"✅ 기본 Python 모듈: {sum(results.values())}/{len(basic_modules)}")
    
    # 외부 패키지들
    try:
        import cv2
        print("✅ OpenCV 사용 가능")
        results['opencv'] = True
    except ImportError:
        print("❌ OpenCV 없음 (pip install opencv-python)")
        results['opencv'] = False
    
    try:
        import numpy as np
        print("✅ NumPy 사용 가능")
        results['numpy'] = True
    except ImportError:
        print("❌ NumPy 없음 (pip install numpy)")
        results['numpy'] = False
    
    try:
        from PIL import Image
        print("✅ Pillow 사용 가능")
        results['pillow'] = True
    except ImportError:
        print("❌ Pillow 없음 (pip install pillow)")
        results['pillow'] = False
    
    try:
        import torch
        print(f"✅ PyTorch 사용 가능 (CUDA: {torch.cuda.is_available()})")
        results['pytorch'] = True
        results['cuda'] = torch.cuda.is_available()
    except ImportError:
        print("❌ PyTorch 없음 (고급 AI 기능 제한)")
        results['pytorch'] = False
        results['cuda'] = False
    
    try:
        from diffusers import StableDiffusionPipeline
        print("✅ Diffusers 사용 가능")
        results['diffusers'] = True
    except ImportError:
        print("❌ Diffusers 없음 (고급 AI 기능 제한)")
        results['diffusers'] = False
    
    try:
        from realesrgan import RealESRGANer
        print("✅ Real-ESRGAN 사용 가능")
        results['realesrgan'] = True
    except ImportError:
        print("❌ Real-ESRGAN 없음 (업스케일링 제한)")
        results['realesrgan'] = False
    
    return results

def create_test_json():
    """테스트용 JSON 데이터 생성"""
    print("\n🎨 테스트 데이터 생성")
    print("-" * 30)
    
    try:
        # 간단한 이미지 데이터 (1x1 투명 PNG)
        # 최소한의 PNG 헤더 + IDAT + IEND
        minimal_png = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\x0f\x00\x00\x01\x00\x01\x00\x18\xdd\x8d\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        
        # Base64 인코딩
        data_url = f"data:image/png;base64,{base64.b64encode(minimal_png).decode()}"
        
        # Chrome Extension 형식 JSON
        test_data = {
            "session_id": f"test_session_{int(time.time())}",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "image_count": 1,
            "images": [{
                "url": data_url,
                "filename": "test_image.png",
                "timestamp": int(time.time()),
                "type": "generated"
            }]
        }
        
        # 파일 저장
        with open("test_simple.json", "w") as f:
            json.dump(test_data, f, indent=2)
        
        print("✅ 테스트 JSON 생성 완료: test_simple.json")
        return "test_simple.json"
        
    except Exception as e:
        print(f"❌ 테스트 JSON 생성 실패: {e}")
        return None

def test_basic_functionality():
    """기본 기능 테스트"""
    print("\n🔧 기본 기능 테스트")
    print("-" * 30)
    
    results = {}
    
    # JSON 읽기/쓰기 테스트
    try:
        test_data = {"test": "data"}
        with open("test_temp.json", "w") as f:
            json.dump(test_data, f)
        
        with open("test_temp.json", "r") as f:
            loaded_data = json.load(f)
        
        os.remove("test_temp.json")
        
        if loaded_data == test_data:
            print("✅ JSON 읽기/쓰기 정상")
            results['json_io'] = True
        else:
            print("❌ JSON 데이터 불일치")
            results['json_io'] = False
            
    except Exception as e:
        print(f"❌ JSON 처리 실패: {e}")
        results['json_io'] = False
    
    # Base64 인코딩/디코딩 테스트
    try:
        test_string = "Hello, World!"
        encoded = base64.b64encode(test_string.encode()).decode()
        decoded = base64.b64decode(encoded).decode()
        
        if decoded == test_string:
            print("✅ Base64 인코딩/디코딩 정상")
            results['base64'] = True
        else:
            print("❌ Base64 처리 오류")
            results['base64'] = False
            
    except Exception as e:
        print(f"❌ Base64 처리 실패: {e}")
        results['base64'] = False
    
    # 파일 시스템 접근 테스트
    try:
        test_file = "test_filesystem.txt"
        with open(test_file, "w") as f:
            f.write("test")
        
        if os.path.exists(test_file):
            os.remove(test_file)
            print("✅ 파일 시스템 접근 정상")
            results['filesystem'] = True
        else:
            print("❌ 파일 생성 실패")
            results['filesystem'] = False
            
    except Exception as e:
        print(f"❌ 파일 시스템 오류: {e}")
        results['filesystem'] = False
    
    return results

def test_ffmpeg_available():
    """FFmpeg 사용 가능성 테스트"""
    print("\n🎬 FFmpeg 테스트")
    print("-" * 30)
    
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg 사용 가능: {version_line}")
            return True
        else:
            print("❌ FFmpeg 실행 실패")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ FFmpeg 타임아웃")
        return False
    except FileNotFoundError:
        print("❌ FFmpeg 없음 (brew install ffmpeg)")
        return False
    except Exception as e:
        print(f"❌ FFmpeg 테스트 실패: {e}")
        return False

def test_project_files():
    """프로젝트 파일 존재 확인"""
    print("\n📁 프로젝트 파일 테스트")
    print("-" * 30)
    
    expected_files = [
        'colab_advanced_ai_video.ipynb',
        'advanced_ai_video_generator.py',
        'riff_optimizer.py',
        'COLAB_VIDEO_GENERATOR.py'
    ]
    
    results = {}
    for file in expected_files:
        if os.path.exists(file):
            print(f"✅ {file} 존재")
            results[file] = True
        else:
            print(f"❌ {file} 없음")
            results[file] = False
    
    return results

def run_simple_tests():
    """간단한 테스트 실행"""
    print("🧪 Advanced AI Video Pipeline - Simple Test")
    print("=" * 50)
    
    test_results = {}
    
    # 1. 모듈 임포트 테스트
    test_results['modules'] = test_modules_import()
    
    # 2. 기본 기능 테스트
    test_results['basic_functions'] = test_basic_functionality()
    
    # 3. 테스트 데이터 생성
    test_json_path = create_test_json()
    test_results['test_data'] = test_json_path is not None
    
    # 4. FFmpeg 테스트
    test_results['ffmpeg'] = test_ffmpeg_available()
    
    # 5. 프로젝트 파일 체크
    test_results['project_files'] = test_project_files()
    
    # 결과 요약
    print("\n" + "=" * 50)
    print("📊 테스트 결과 요약")
    print("=" * 50)
    
    # 모듈 상태
    modules = test_results['modules']
    print("🐍 Python 패키지:")
    print(f"  NumPy: {'✅' if modules.get('numpy') else '❌'}")
    print(f"  Pillow: {'✅' if modules.get('pillow') else '❌'}")
    print(f"  OpenCV: {'✅' if modules.get('opencv') else '❌'}")
    print(f"  PyTorch: {'✅' if modules.get('pytorch') else '❌'}")
    print(f"  CUDA: {'✅' if modules.get('cuda') else '❌'}")
    print(f"  Diffusers: {'✅' if modules.get('diffusers') else '❌'}")
    print(f"  Real-ESRGAN: {'✅' if modules.get('realesrgan') else '❌'}")
    
    # 기본 기능 상태
    basic = test_results['basic_functions']
    print(f"\n🔧 기본 기능:")
    print(f"  JSON 처리: {'✅' if basic.get('json_io') else '❌'}")
    print(f"  Base64: {'✅' if basic.get('base64') else '❌'}")
    print(f"  파일 시스템: {'✅' if basic.get('filesystem') else '❌'}")
    print(f"  테스트 데이터: {'✅' if test_results['test_data'] else '❌'}")
    print(f"  FFmpeg: {'✅' if test_results['ffmpeg'] else '❌'}")
    
    # 프로젝트 파일
    project_files = test_results['project_files']
    print(f"\n📁 프로젝트 파일:")
    for filename, exists in project_files.items():
        print(f"  {filename}: {'✅' if exists else '❌'}")
    
    # 준비도 평가
    essential_count = sum([
        basic.get('json_io', False),
        basic.get('base64', False),
        basic.get('filesystem', False),
        test_results['test_data']
    ])
    
    video_count = sum([
        modules.get('opencv', False) or modules.get('pillow', False),
        test_results['ffmpeg']
    ])
    
    advanced_count = sum([
        modules.get('pytorch', False),
        modules.get('cuda', False),
        modules.get('diffusers', False),
        modules.get('realesrgan', False)
    ])
    
    project_count = sum(project_files.values())
    
    print(f"\n🎯 시스템 준비도:")
    print(f"  필수 기능: {essential_count}/4")
    print(f"  비디오 처리: {video_count}/2") 
    print(f"  고급 AI: {advanced_count}/4")
    print(f"  프로젝트 파일: {project_count}/{len(project_files)}")
    
    # 총 평가
    if essential_count >= 3 and video_count >= 1:
        print("\n✅ 기본 비디오 생성 준비 완료")
    else:
        print("\n❌ 기본 설정 부족")
        print("   필요한 패키지: pip install pillow opencv-python")
        if not test_results['ffmpeg']:
            print("   FFmpeg 설치: brew install ffmpeg")
    
    if advanced_count >= 2:
        print("🚀 고급 AI 기능 사용 가능")
    else:
        print("⚠️ 고급 AI 기능 제한됨 (선택사항)")
    
    if project_count == len(project_files):
        print("📂 모든 프로젝트 파일 준비됨")
    else:
        print("📂 일부 프로젝트 파일 누락")
    
    return test_results

if __name__ == "__main__":
    run_simple_tests()