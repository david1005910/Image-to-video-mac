#!/bin/bash
# 고급 AI 비디오 파이프라인 필수 패키지 설치

echo "🚀 고급 AI 비디오 파이프라인 설치 시작"
echo "=" * 50

# 기본 Python 패키지
echo "📦 기본 패키지 설치 중..."
pip3 install pillow numpy opencv-python

# 비디오 처리
echo "🎬 비디오 처리 패키지 설치 중..."
pip3 install moviepy imageio imageio-ffmpeg

# AI 패키지 (선택사항)
echo "🧠 AI 패키지 설치 중 (시간이 오래 걸릴 수 있음)..."
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# FFmpeg 확인
echo "🔍 FFmpeg 확인 중..."
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg 이미 설치됨"
else
    echo "⚠️ FFmpeg 설치 필요"
    if command -v brew &> /dev/null; then
        echo "🍺 Homebrew로 FFmpeg 설치 중..."
        brew install ffmpeg
    else
        echo "❌ Homebrew가 없습니다. FFmpeg를 수동으로 설치하세요"
        echo "https://ffmpeg.org/download.html"
    fi
fi

echo "✅ 설치 완료!"