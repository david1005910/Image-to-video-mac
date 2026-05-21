# 📹 비디오 생성 완전 가이드

## 🎯 전체 프로세스 개요

```
[이미지 수집] → [JSON 생성] → [Colab 업로드] → [비디오 렌더링] → [다운로드]
```

---

## 📌 Step 1: Chrome Extension에서 이미지 준비

### 1-1. Extension 설치
1. Chrome 브라우저 열기
2. `chrome://extensions/` 접속
3. "개발자 모드" ON
4. "압축 해제된 확장 프로그램 로드"
5. `chrome-extension` 폴더 선택

### 1-2. 이미지 수집 (3가지 방법)

#### 방법 A: Midjourney/Discord에서 자동 수집
```
1. Discord 또는 Midjourney.com 접속
2. Extension 아이콘 클릭
3. "📸 이미지 수집 시작" 클릭
4. 페이지 스크롤하며 이미지 자동 수집
```

#### 방법 B: AI 이미지 생성
```
1. Extension 팝업에서 "🎨 AI 이미지 생성" 클릭
2. 프롬프트 입력 (예: "beautiful sunset over mountains")
3. "🚀 생성 시작" 클릭
4. 10-20초 대기
```

#### 방법 C: 로컬 파일 업로드
```
1. "📁 이미지 파일 업로드" 클릭
2. 이미지 파일 선택 (여러 개 가능)
3. 자동으로 컬렉션에 추가
```

### 1-3. 이미지 관리
- **확인**: 팝업 하단 그리드에서 썸네일 확인
- **삭제**: 이미지 위 마우스 호버 → × 버튼 클릭
- **초기화**: "🗑️ 초기화" 버튼으로 전체 삭제

---

## 📌 Step 2: JSON 파일 생성 및 다운로드

### 2-1. Colab 연동 패널 열기
```
1. Extension 팝업에서 "Colab에서 편집" 버튼 클릭
2. Drive 업로드 패널이 열림
3. Session ID 자동 생성 (예: session_abc123)
```

### 2-2. JSON 다운로드
```
1. "📤 Drive 업로드 시작" 클릭
2. JSON 파일이 자동으로 다운로드됨
   - 파일명: midjourney_images_session_xxx.json
   - 위치: 다운로드 폴더
```

### 2-3. JSON 파일 구조
```json
{
  "session_id": "session_abc123",
  "created_at": "2024-05-21T12:00:00",
  "image_count": 10,
  "images": [
    {
      "url": "data:image/png;base64,...",  // 이미지 데이터
      "filename": "image_001.png",
      "timestamp": 1716288000000,
      "type": "generated"  // collected/generated/uploaded
    }
  ]
}
```

---

## 📌 Step 3: Google Colab에서 비디오 생성

### 3-1. Colab 노트북 열기

#### 옵션 1: 간단한 버전 (추천) ⭐
```
1. Google Colab 접속 (https://colab.research.google.com)
2. 파일 → 노트북 업로드
3. "colab_simple_video.ipynb" 선택
```

#### 옵션 2: GitHub에서 열기
```
https://colab.research.google.com/github/[your-repo]/blob/main/colab_simple_video.ipynb
```

### 3-2. GPU 설정 (선택사항, 더 빠른 처리)
```
1. 런타임 → 런타임 유형 변경
2. 하드웨어 가속기: GPU (T4)
3. 저장
```

### 3-3. 비디오 생성 실행

#### 🚀 빠른 실행 (한 번에 모든 작업)
```python
# 첫 번째 셀만 실행하면 됩니다!
# [▶️ 실행] 버튼 클릭

# 1. 라이브러리 자동 설치
# 2. "파일 선택" 창 열림
# 3. JSON 파일 업로드
# 4. 자동으로 비디오 생성
# 5. 미리보기 표시
# 6. 자동 다운로드
```

실행 과정:
```
🎬 Chrome Extension 비디오 생성기
==================================================

📤 Chrome Extension JSON 파일을 업로드하세요:
[파일 선택 버튼 클릭]

✅ 10개 이미지 로드
✓ 이미지 1/10 처리
✓ 이미지 2/10 처리
...

🎬 비디오 생성 중...
✅ 비디오 생성 완료!
📹 길이: 30초
📁 파일: session_abc123_video.mp4

[비디오 미리보기 표시]

💾 다운로드 중...
```

---

## 📌 Step 4: 비디오 커스터마이징 (선택사항)

### 4-1. 기본 설정
```python
CONFIG = {
    'duration_per_image': 3.0,    # 이미지당 표시 시간(초)
    'resolution': (1920, 1080),   # Full HD
    'transition': 0.5,            # 전환 효과 시간
    'fps': 30,                    # 프레임레이트
    'quality': 'high'             # 품질
}
```

### 4-2. 해상도 옵션
- **SD**: (640, 480)
- **HD**: (1280, 720)
- **Full HD**: (1920, 1080) ← 기본값
- **4K**: (3840, 2160)

### 4-3. 효과 옵션

#### Ken Burns 효과 (줌/패닝)
```python
enable_ken_burns = True
zoom_ratio = 1.2  # 20% 줌
```

#### 전환 효과
```python
transition_type = 'crossfade'  # 크로스페이드
transition_duration = 0.5       # 0.5초
```

#### 색상 필터
```python
color_filter = 'cinematic'  # 시네마틱
# 옵션: cinematic, vintage, cold, warm, none
```

### 4-4. BGM 추가
```python
add_bgm = True  # 앰비언트 사운드 자동 생성
```

---

## 📌 Step 5: 결과물 활용

### 5-1. 다운로드된 파일
```
파일명: session_xxx_video.mp4
크기: 약 10-50MB (품질에 따라)
형식: MP4 (H.264 코덱)
```

### 5-2. 활용 방법

#### YouTube 업로드
```
1. YouTube Studio 접속
2. 동영상 업로드
3. 제목/설명 작성
4. 공개 설정
```

#### SNS 공유
- **Instagram**: 최대 60초, 9:16 비율 권장
- **Twitter**: 최대 2분 20초
- **TikTok**: 최대 10분, 9:16 비율
- **Facebook**: 최대 240분

#### 편집 도구에서 추가 편집
- Adobe Premiere Pro
- Final Cut Pro
- DaVinci Resolve
- iMovie

---

## 🔧 문제 해결

### 문제: Extension 아이콘이 안 보임
```
해결: 
1. chrome://extensions/ 에서 Extension 새로고침
2. 브라우저 재시작
3. 퍼즐 아이콘 클릭 → Extension 고정
```

### 문제: JSON 다운로드 안 됨
```
해결:
1. 브라우저 다운로드 설정 확인
2. 팝업 차단 해제
3. 다운로드 폴더 권한 확인
```

### 문제: Colab에서 메모리 부족
```
해결:
1. 런타임 → 세션 다시 시작
2. 이미지 수 줄이기 (최대 30개 권장)
3. 해상도 낮추기 (HD로 변경)
```

### 문제: 비디오가 재생 안 됨
```
해결:
1. VLC Player 사용
2. 코덱 팩 설치
3. 브라우저에서 재생 (Chrome/Firefox)
```

---

## ⏱️ 예상 시간

| 단계 | 소요 시간 |
|------|-----------|
| Extension 설치 | 1분 |
| 이미지 수집 | 2-5분 |
| JSON 다운로드 | 10초 |
| Colab 설정 | 1분 |
| 비디오 생성 | 1-3분 |
| **총 시간** | **5-10분** |

---

## 💡 프로 팁

### 1. 이미지 최적화
- **일관된 스타일**: 비슷한 스타일의 이미지 사용
- **해상도 통일**: 모든 이미지 해상도 비슷하게
- **순서 정리**: 스토리 흐름에 맞게 정렬

### 2. 효과 조합
```python
# 최상의 조합
enable_ken_burns = True      # 움직임
color_filter = 'cinematic'   # 영화같은 느낌
transition = 'crossfade'     # 부드러운 전환
add_bgm = True               # 배경음악
```

### 3. 품질 vs 속도
- **빠른 테스트**: quality='low', resolution=(1280,720)
- **최종 출력**: quality='ultra', resolution=(1920,1080)

### 4. 배치 처리
```python
# 여러 세션 한 번에 처리
sessions = ['session1.json', 'session2.json', 'session3.json']
for session in sessions:
    generate_video(session)
```

---

## 📊 성능 벤치마크

| 이미지 수 | 비디오 길이 | GPU 없음 | GPU (T4) | 파일 크기 |
|----------|------------|---------|----------|-----------|
| 5개 | 15초 | 30초 | 15초 | ~5MB |
| 10개 | 30초 | 1분 | 30초 | ~12MB |
| 20개 | 60초 | 3분 | 1분 | ~25MB |
| 50개 | 150초 | 8분 | 3분 | ~60MB |

---

## 🎬 예시 시나리오

### 시나리오 1: 포트폴리오 비디오
```
1. Midjourney에서 작품 10개 수집
2. Ken Burns 효과 + 시네마틱 필터
3. 이미지당 5초, 총 50초 비디오
4. YouTube에 업로드
```

### 시나리오 2: SNS 쇼츠
```
1. AI로 5개 이미지 생성
2. 빠른 전환 (0.2초)
3. 이미지당 2초, 총 10초
4. Instagram Reels 업로드
```

### 시나리오 3: 프레젠테이션
```
1. 로컬 이미지 20개 업로드
2. 전환 효과 없음
3. 이미지당 10초, 총 3분 20초
4. PowerPoint에 삽입
```

---

## 🔗 관련 리소스

- [Chrome Extension 설치 가이드](EXTENSION_INSTALL_GUIDE.md)
- [Colab 노트북](colab_simple_video.ipynb)
- [Python 스크립트](COLAB_VIDEO_GENERATOR.py)
- [문제 해결 FAQ](EXTENSION_TEST.md)

---

*Chrome Extension Video Generator - 완전 가이드*
*버전 1.0 | 2024년 5월*