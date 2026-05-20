# 🎬 Midjourney to Video Creator Chrome Extension

Midjourney에서 생성한 이미지를 자동으로 수집하고 동영상으로 변환하는 Chrome Extension입니다.

## ✨ 주요 기능

### 1. **자동 이미지 수집**
- Discord 채팅에서 Midjourney 이미지 자동 감지
- Midjourney 웹사이트에서 이미지 수집
- Upscale된 고품질 이미지만 선택 수집
- 실시간 이미지 모니터링

### 2. **동영상 생성**
- 수집된 이미지를 로컬 서버로 전송
- 다양한 트랜지션 효과 적용
- 켄번즈, 줌, 슬라이드 등 모션 효과
- 색상 필터 및 프레임 효과

### 3. **편리한 UI**
- 플로팅 버튼으로 쉬운 접근
- 실시간 이미지 미리보기
- 수집 상태 모니터링
- 원클릭 동영상 생성

## 🚀 설치 방법

### 1. Extension 설치
1. Chrome 브라우저에서 `chrome://extensions/` 접속
2. "개발자 모드" 활성화
3. "압축 해제된 확장 프로그램 로드" 클릭
4. `chrome-extension` 폴더 선택

### 2. 로컬 서버 실행
```bash
# 서버 실행
npm run dev

# 워커 실행 (별도 터미널)
npm run worker
```

### 3. 사용 준비
- Discord 또는 Midjourney.com 접속
- 페이지 우측 하단의 🎬 버튼 확인

## 📖 사용 방법

### Discord에서 사용
1. Midjourney가 활성화된 Discord 서버/채널 접속
2. 우측 하단 🎬 버튼 클릭
3. "📸 이미지 수집 시작" 클릭
4. 채팅을 스크롤하며 이미지 수집
5. "🎬 동영상 생성" 클릭

### Midjourney 웹사이트에서 사용
1. www.midjourney.com 접속 및 로그인
2. Gallery 또는 생성 페이지 이동
3. Extension으로 이미지 수집
4. 동영상 생성

## ⚙️ 설정 옵션

### 수집 설정
- **자동 수집**: 페이지 로드 시 자동으로 이미지 수집 시작
- **Upscale만**: 고품질 Upscale 이미지만 수집
- **자동 스크롤**: 자동으로 페이지 스크롤하며 수집

### 동영상 설정
- **스타일**: 슬라이드쇼, 켄번즈, 콜라주
- **이미지당 시간**: 1-10초
- **전환 효과**: 페이드, 줌, 슬라이드, 회전
- **색상 효과**: 세피아, 흑백, 빈티지 등
- **모션 효과**: 켄번즈, 흔들림, 펄스 등

## 🔧 기술 구조

### Extension 구성
```
chrome-extension/
├── manifest.json      # Extension 설정
├── content.js         # 페이지 내 스크립트
├── background.js      # 백그라운드 서비스
├── popup.html/js      # 팝업 UI
└── style.css          # 스타일
```

### 이미지 수집 프로세스
1. **감지**: MutationObserver로 DOM 변화 감지
2. **필터링**: Midjourney CDN URL 패턴 매칭
3. **수집**: 이미지 URL과 메타데이터 저장
4. **저장**: Chrome Storage API 활용

### 동영상 생성 프로세스
1. **다운로드**: 수집된 이미지 Blob 변환
2. **업로드**: FormData로 로컬 서버 전송
3. **렌더링**: FFmpeg로 동영상 생성
4. **다운로드**: 완성된 MP4 파일 제공

## ⚠️ 주의사항

1. **로컬 서버 필수**
   - localhost:3000에서 서버가 실행되어야 함
   - 서버와 워커 모두 실행 필요

2. **권한 요구사항**
   - Discord/Midjourney 사이트 접근 권한
   - 이미지 다운로드 권한
   - Storage 권한

3. **저작권**
   - Midjourney 이용 약관 준수
   - 생성된 이미지의 저작권 확인
   - 상업적 사용 시 라이선스 확인

## 🛠️ 문제 해결

### Extension이 작동하지 않을 때
1. 개발자 모드 확인
2. Extension 새로고침
3. 페이지 새로고침

### 이미지가 수집되지 않을 때
1. Discord/Midjourney 로그인 확인
2. 이미지 로딩 대기
3. 수동으로 "수집 시작" 클릭

### 동영상 생성 실패 시
1. 로컬 서버 실행 확인
2. 네트워크 연결 확인
3. 이미지 개수 확인 (최소 1개 필요)

## 📊 성능 최적화

- 이미지 중복 제거
- 대용량 이미지 압축
- 비동기 처리
- 메모리 관리

## 🔒 보안

- CORS 정책 준수
- HTTPS 통신
- 로컬 서버만 접근 가능
- 개인정보 미수집

## 📝 라이선스

MIT License - 자유롭게 사용 가능하나 Midjourney 약관 준수 필요

## 🤝 기여

버그 리포트 및 기능 제안 환영!

---

Made with ❤️ for Midjourney creators