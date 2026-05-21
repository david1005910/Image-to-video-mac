#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Advanced AI Video Pipeline Test Suite
전체 고급 AI 비디오 생성 파이프라인 테스트
"""

import os
import sys
import json
import time
import base64
from pathlib import Path
from PIL import Image
import numpy as np
from io import BytesIO

# 프로젝트 모듈 임포트
try:
    from advanced_ai_video_generator import AdvancedAIVideoPipeline
    from riff_optimizer import AdvancedVideoProcessor
    AI_MODULES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ AI 모듈 임포트 실패: {e}")
    AI_MODULES_AVAILABLE = False

def create_test_json_data(num_images=5):
    """테스트용 Chrome Extension JSON 데이터 생성"""
    print(f"🎨 {num_images}개 테스트 이미지 생성 중...")
    
    # 간단한 그라디언트 이미지들 생성
    test_images = []
    
    for i in range(num_images):
        # 그라디언트 이미지 생성
        width, height = 512, 512
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # 각 이미지마다 다른 색상 패턴
        for y in range(height):
            for x in range(width):
                r = int(255 * (x / width) * (0.5 + 0.5 * np.sin(i * np.pi / num_images)))
                g = int(255 * (y / height) * (0.5 + 0.5 * np.cos(i * np.pi / num_images)))
                b = int(255 * ((x + y) / (width + height)) * (0.5 + 0.5 * np.sin(i * np.pi / 2)))
                image[y, x] = [r, g, b]
        
        # PIL Image로 변환
        pil_image = Image.fromarray(image)
        
        # Data URL로 변환
        buffer = BytesIO()
        pil_image.save(buffer, format='PNG')
        img_bytes = buffer.getvalue()
        data_url = f"data:image/png;base64,{base64.b64encode(img_bytes).decode()}"
        
        test_images.append({
            "url": data_url,
            "filename": f"test_image_{i+1:02d}.png",
            "timestamp": int(time.time()) + i,
            "type": "generated",
            "prompt": f"Test gradient pattern {i+1}"
        })
        
        print(f"  ✅ 테스트 이미지 {i+1}/{num_images} 생성 완료")
    
    # Chrome Extension JSON 형식
    test_data = {
        "session_id": f"test_session_{int(time.time())}",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "image_count": len(test_images),
        "images": test_images
    }
    
    return test_data

def save_test_json(test_data, output_path):
    """테스트 JSON 파일 저장"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 테스트 JSON 저장: {output_path}")
    return output_path

def test_basic_functionality():
    """기본 기능 테스트"""
    print("🔍 기본 기능 테스트")
    print("-" * 30)
    
    # 1. 테스트 데이터 생성
    test_data = create_test_json_data(3)  # 작은 테스트
    test_json_path = "./test_data.json"
    save_test_json(test_data, test_json_path)
    
    # 2. 기본 파이프라인 테스트
    if AI_MODULES_AVAILABLE:
        try:
            print("🧠 AI 파이프라인 초기화...")
            pipeline = AdvancedAIVideoPipeline("./test_output")
            
            # 설정을 테스트용으로 조정
            pipeline.config.update({
                'output_resolution': (640, 480),  # 작은 해상도
                'target_fps': 15,                 # 낮은 FPS
                'video_length_per_image': 1.0,    # 짧은 길이
                'use_upscaling': False,           # 업스케일링 비활성화
                'use_depth_estimation': False,    # Depth 비활성화
                'quality': 'medium'
            })
            
            print("🚀 파이프라인 실행...")
            output_path = pipeline.run_complete_pipeline(test_json_path)
            
            if output_path and os.path.exists(output_path):
                print(f"✅ 기본 테스트 성공: {output_path}")
                return output_path
            else:
                print("❌ 기본 테스트 실패: 출력 파일 없음")
                return None
                
        except Exception as e:
            print(f"❌ 기본 테스트 실패: {e}")
            return None
    else:
        print("⚠️ AI 모듈을 사용할 수 없어 기본 테스트를 건너뜁니다")
        return None

def test_riff_optimization(input_video_path):
    """RIFF 최적화 테스트"""
    print("\n🎯 RIFF 최적화 테스트")
    print("-" * 30)
    
    if not input_video_path or not os.path.exists(input_video_path):
        print("❌ 입력 비디오가 없어 RIFF 테스트를 건너뜁니다")
        return False
    
    try:
        processor = AdvancedVideoProcessor("./test_riff_output")
        session_id = f"riff_test_{int(time.time())}"
        
        print("🔧 RIFF 최적화 실행...")
        results = processor.process_ai_video_with_riff_optimization(
            input_video_path, session_id
        )
        
        if results and results['outputs']['riff_optimized']['success']:
            print("✅ RIFF 최적화 테스트 성공")
            return True
        else:
            print("❌ RIFF 최적화 테스트 실패")
            return False
            
    except Exception as e:
        print(f"❌ RIFF 최적화 테스트 실패: {e}")
        return False

def test_performance_benchmark():
    """성능 벤치마크 테스트"""
    print("\n📊 성능 벤치마크")
    print("-" * 30)
    
    test_scenarios = [
        {'name': '소형 테스트', 'images': 3, 'resolution': (480, 360), 'fps': 15},
        {'name': '중형 테스트', 'images': 5, 'resolution': (720, 480), 'fps': 24},
        {'name': '대형 테스트', 'images': 10, 'resolution': (1280, 720), 'fps': 30}
    ]
    
    results = {}
    
    for scenario in test_scenarios:
        if not AI_MODULES_AVAILABLE:
            print(f"⚠️ {scenario['name']}: AI 모듈 없음으로 건너뜀")
            continue
            
        print(f"🏃 {scenario['name']} 실행 중...")
        
        try:
            # 테스트 데이터 생성
            test_data = create_test_json_data(scenario['images'])
            test_json_path = f"./test_{scenario['name'].replace(' ', '_').lower()}.json"
            save_test_json(test_data, test_json_path)
            
            # 파이프라인 설정
            pipeline = AdvancedAIVideoPipeline(f"./benchmark_output_{scenario['name'].replace(' ', '_').lower()}")
            pipeline.config.update({
                'output_resolution': scenario['resolution'],
                'target_fps': scenario['fps'],
                'video_length_per_image': 1.0,
                'use_upscaling': False,
                'use_depth_estimation': False,
                'quality': 'medium'
            })
            
            start_time = time.time()
            output_path = pipeline.run_complete_pipeline(test_json_path)
            processing_time = time.time() - start_time
            
            # 결과 파일 크기
            file_size_mb = os.path.getsize(output_path) / (1024*1024) if output_path and os.path.exists(output_path) else 0
            
            results[scenario['name']] = {
                'success': output_path is not None,
                'processing_time': processing_time,
                'file_size_mb': file_size_mb,
                'images': scenario['images'],
                'resolution': f"{scenario['resolution'][0]}x{scenario['resolution'][1]}",
                'fps': scenario['fps']
            }
            
            print(f"  ✅ 완료: {processing_time:.1f}초, {file_size_mb:.1f}MB")
            
        except Exception as e:
            print(f"  ❌ 실패: {e}")
            results[scenario['name']] = {'success': False, 'error': str(e)}
    
    # 벤치마크 결과 출력
    print("\n📈 벤치마크 결과:")
    for name, result in results.items():
        if result['success']:
            images_per_sec = result['images'] / result['processing_time']
            print(f"  {name}:")
            print(f"    처리 시간: {result['processing_time']:.1f}초")
            print(f"    이미지/초: {images_per_sec:.2f}")
            print(f"    파일 크기: {result['file_size_mb']:.1f}MB")
        else:
            print(f"  {name}: 실패")
    
    return results

def run_comprehensive_test():
    """종합 테스트 실행"""
    print("🧪 고급 AI 비디오 파이프라인 종합 테스트")
    print("=" * 60)
    
    test_results = {
        'basic_functionality': False,
        'riff_optimization': False,
        'performance_benchmark': None
    }\n    \n    # 1. 기본 기능 테스트\n    print(\"\\n1️⃣ 기본 기능 테스트 시작...\")\n    basic_output = test_basic_functionality()\n    test_results['basic_functionality'] = basic_output is not None\n    \n    # 2. RIFF 최적화 테스트\n    print(\"\\n2️⃣ RIFF 최적화 테스트 시작...\")\n    test_results['riff_optimization'] = test_riff_optimization(basic_output)\n    \n    # 3. 성능 벤치마크\n    print(\"\\n3️⃣ 성능 벤치마크 시작...\")\n    test_results['performance_benchmark'] = test_performance_benchmark()\n    \n    # 최종 결과\n    print(\"\\n\" + \"=\" * 60)\n    print(\"🏁 종합 테스트 결과\")\n    print(\"=\" * 60)\n    \n    print(f\"✅ 기본 기능: {'통과' if test_results['basic_functionality'] else '실패'}\")\n    print(f\"✅ RIFF 최적화: {'통과' if test_results['riff_optimization'] else '실패'}\")\n    print(f\"✅ 성능 벤치마크: {'완료' if test_results['performance_benchmark'] else '실패'}\")\n    \n    # 전체 성공률\n    success_count = sum([test_results['basic_functionality'], test_results['riff_optimization']])\n    if test_results['performance_benchmark']:\n        benchmark_success = sum(1 for r in test_results['performance_benchmark'].values() if r.get('success', False))\n        success_count += benchmark_success > 0\n    \n    print(f\"\\n🎯 전체 성공률: {success_count}/3\")\n    \n    if success_count >= 2:\n        print(\"🎉 고급 AI 비디오 파이프라인이 정상적으로 작동합니다!\")\n    else:\n        print(\"⚠️ 일부 기능에 문제가 있습니다. 로그를 확인하세요.\")\n    \n    return test_results\n\ndef interactive_test():\n    \"\"\"대화형 테스트 모드\"\"\"\n    print(\"🎮 대화형 테스트 모드\")\n    print(\"=\" * 30)\n    \n    while True:\n        print(\"\\n선택하세요:\")\n        print(\"1. 기본 기능 테스트\")\n        print(\"2. RIFF 최적화 테스트\")\n        print(\"3. 성능 벤치마크\")\n        print(\"4. 종합 테스트\")\n        print(\"5. 종료\")\n        \n        choice = input(\"\\n번호를 입력하세요 (1-5): \").strip()\n        \n        if choice == '1':\n            test_basic_functionality()\n        elif choice == '2':\n            video_path = input(\"비디오 파일 경로를 입력하세요: \").strip()\n            test_riff_optimization(video_path)\n        elif choice == '3':\n            test_performance_benchmark()\n        elif choice == '4':\n            run_comprehensive_test()\n        elif choice == '5':\n            print(\"👋 테스트 종료\")\n            break\n        else:\n            print(\"❌ 잘못된 선택입니다\")\n\ndef main():\n    \"\"\"메인 함수\"\"\"\n    print(\"🧪 Advanced AI Video Pipeline Test Suite\")\n    print(\"=\" * 50)\n    \n    if len(sys.argv) > 1:\n        mode = sys.argv[1].lower()\n        \n        if mode == 'comprehensive':\n            run_comprehensive_test()\n        elif mode == 'basic':\n            test_basic_functionality()\n        elif mode == 'riff':\n            video_path = sys.argv[2] if len(sys.argv) > 2 else input(\"비디오 경로: \")\n            test_riff_optimization(video_path)\n        elif mode == 'benchmark':\n            test_performance_benchmark()\n        else:\n            print(f\"❌ 알 수 없는 모드: {mode}\")\n            print(\"사용법: python test_advanced_pipeline.py [comprehensive|basic|riff|benchmark]\")\n    else:\n        interactive_test()\n\nif __name__ == \"__main__\":\n    main()