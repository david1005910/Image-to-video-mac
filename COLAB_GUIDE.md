# 📺 Chrome Extension + Colab 영상 편집 통합 가이드

## 🚀 빠른 시작

### 1. Chrome Extension 설정
1. Extension 설치 후 팝업 열기
2. 이미지 수집 또는 AI 생성
3. "Colab에서 편집" 버튼 클릭
4. Session ID 복사

### 2. Colab 노트북 실행
1. [colab_video_editor.ipynb 열기](https://colab.research.google.com/)
2. 런타임 → GPU 설정
3. Session ID 입력
4. 편집 실행

---

## 🎬 고급 영상 편집 기능

### MoviePy 기능
- **기본 편집**: 자르기, 붙이기, 회전, 크롭
- **전환 효과**: 페이드, 슬라이드, 줌, 회전
- **모션 효과**: Ken Burns, 패닝, 틸트
- **텍스트/자막**: 다국어 지원, 애니메이션
- **필터**: 색보정, 블러, 샤프닝, 빈티지

### OpenCV 기능
- **영상 안정화**: 흔들림 보정
- **객체 추적**: 모션 트래킹
- **얼굴 인식**: 자동 포커스
- **배경 제거**: 크로마키, 세그멘테이션
- **특수 효과**: 모자이크, 왜곡, 모핑

### FFmpeg 기능
- **코덱 변환**: H.264, H.265, VP9, AV1
- **해상도 조절**: 4K, 1080p, 720p
- **프레임레이트**: 24/30/60/120 fps
- **오디오 처리**: 노이즈 제거, 이퀄라이저
- **스트리밍**: HLS, DASH 변환

---

## 📁 Google Drive 연동

### OAuth2 설정 (선택사항)
```json
// manifest.json에 추가
"oauth2": {
  "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
  "scopes": [
    "https://www.googleapis.com/auth/drive.file"
  ]
}
```

### 자동 업로드 프로세스
1. Extension에서 이미지 수집
2. Session ID 자동 생성
3. Google Drive 폴더 생성
4. 이미지 + 메타데이터 업로드
5. Colab에서 자동 로드

---

## 🔧 Colab 편집 파라미터

### 비디오 설정
```python
VIDEO_CONFIG = {
    # 해상도
    "resolution": (1920, 1080),  # 4K: (3840, 2160)
    "fps": 30,                   # 24, 30, 60
    
    # 효과
    "transition_type": "crossfade",  # slide, zoom, rotate
    "transition_duration": 0.5,
    "enable_ken_burns": True,
    "zoom_ratio": 1.2,
    
    # 필터
    "color_filter": "cinematic",  # vintage, cold, warm
    "brightness": 1.0,
    "contrast": 1.1,
    "saturation": 1.2,
    
    # 출력
    "output_format": "mp4",
    "codec": "libx264",
    "quality": "high"
}
```

### 고급 효과
```python
# 3D 효과
"enable_3d": True,
"depth_map": "auto",  # AI 깊이 추정

# 모션 블러
"motion_blur": True,
"blur_intensity": 0.5,

# 색상 그레이딩
"lut_file": "cinematic.cube",
"color_space": "rec709",

# AI 향상
"ai_upscale": True,
"ai_interpolation": True,
"ai_denoising": True
```

---

## 🎨 사용 예시

### 1. 슬라이드쇼 스타일
```python
# 심플한 이미지 슬라이드쇼
VIDEO_CONFIG = {
    "duration_per_image": 5.0,
    "transition_type": "crossfade",
    "add_captions": True,
    "bgm_url": "ambient_music.mp3"
}
```

### 2. 다이나믹 몽타주
```python
# 빠른 컷 편집
VIDEO_CONFIG = {
    "duration_per_image": 0.5,
    "transition_type": "none",
    "enable_ken_burns": True,
    "speed_ramp": True
}
```

### 3. 시네마틱 트레일러
```python
# 영화 예고편 스타일
VIDEO_CONFIG = {
    "color_filter": "cinematic",
    "aspect_ratio": "2.35:1",
    "add_letterbox": True,
    "dramatic_music": True
}
```

### 4. 소셜 미디어 최적화
```python
# 인스타그램 릴스/TikTok
VIDEO_CONFIG = {
    "resolution": (1080, 1920),  # 9:16 세로
    "duration_per_image": 2.0,
    "add_trending_music": True,
    "auto_subtitles": True
}
```

---

## 🛠️ 문제 해결

### GPU 메모리 부족
- 해상도 낮추기: 1920x1080 → 1280x720
- 배치 크기 조절
- 모델 경량화 옵션 사용

### 렌더링 속도 개선
- GPU 런타임 사용 (T4 이상)
- 프리셋 조절: ultrafast → medium
- 병렬 처리 활성화

### 품질 향상
- 비트레이트 증가
- CRF 값 낮추기 (15-18)
- 2-pass 인코딩 사용

---

## 📊 성능 벤치마크

| GPU | 해상도 | FPS | 1분 영상 렌더링 시간 |
|-----|--------|-----|-------------------|
| T4 | 720p | 30 | ~2분 |
| T4 | 1080p | 30 | ~5분 |
| V100 | 1080p | 30 | ~2분 |
| V100 | 4K | 30 | ~8분 |
| A100 | 4K | 60 | ~5분 |

---

## 🔗 유용한 링크

- [MoviePy 문서](https://zulko.github.io/moviepy/)
- [OpenCV 튜토리얼](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [FFmpeg 필터 가이드](https://ffmpeg.org/ffmpeg-filters.html)
- [Colab GPU 팁](https://colab.research.google.com/notebooks/gpu.ipynb)

---

## 💡 팁 & 트릭

1. **배치 처리**: 여러 영상을 한 번에 처리
2. **템플릿 저장**: 자주 쓰는 설정 저장
3. **프리뷰 모드**: 저해상도로 빠른 미리보기
4. **캐시 활용**: Drive에 중간 결과 저장
5. **협업**: Colab 노트북 공유로 팀 작업

---

*Chrome Extension + Colab 영상 편집 파이프라인 v1.0*
*MoviePy + OpenCV + FFmpeg 통합 버전*