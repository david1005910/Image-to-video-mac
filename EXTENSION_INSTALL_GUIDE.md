# 📦 Chrome Extension 설치 가이드

## 🚀 설치 방법 (3단계)

### 1단계: Chrome 개발자 모드 활성화
1. Chrome 브라우저 열기
2. 주소창에 입력: `chrome://extensions/`
3. 우측 상단의 **"개발자 모드"** 스위치를 ON으로 변경
   
   ![개발자 모드](https://user-images.githubusercontent.com/xxx/dev-mode.png)

### 2단계: Extension 폴더 로드
1. **"압축 해제된 확장 프로그램 로드"** 버튼 클릭
2. 파일 선택 창에서 다음 경로 선택:
   ```
   /Users/david/Documents/Audio-Video/image-to-video-mac/chrome-extension
   ```
3. "선택" 버튼 클릭

### 3단계: 설치 확인
- Extension이 목록에 나타나는지 확인
- "Midjourney to Video Creator" 카드가 보이면 성공!
- 우측 상단 퍼즐 아이콘 🧩 클릭 → Extension 고정 📌

---

## ✅ 설치 완료 후 확인사항

### Extension이 제대로 설치되었는지 확인:
1. **Extension 목록에서 확인**
   - "Midjourney to Video Creator" 표시
   - "사용" 토글이 ON 상태

2. **아이콘 확인**
   - 브라우저 우측 상단에 🎬 아이콘
   - 아이콘 클릭 시 팝업 창 표시

3. **권한 확인**
   - Discord.com 접근 권한
   - localhost:3000 접근 권한

---

## 🎯 사용 방법

### Discord에서 사용:
1. Discord 웹 버전 접속 (https://discord.com)
2. Midjourney 봇이 있는 채널 이동
3. 페이지 우측 하단 🎬 플로팅 버튼 확인
4. 버튼 클릭 → 패널 열기
5. "📸 이미지 수집 시작" 클릭

### Midjourney.com에서 사용:
1. https://www.midjourney.com 접속
2. 로그인 후 Gallery 이동
3. 동일하게 우측 하단 버튼 사용

---

## 🛠️ 문제 해결

### ❌ "오류가 발생했습니다" 메시지
```bash
# 해결 방법:
1. Extensions 페이지에서 "오류" 버튼 클릭
2. 오류 내용 확인
3. Extension 새로고침 (↻ 버튼)
```

### ❌ 플로팅 버튼이 안 보일 때
```bash
# 해결 방법:
1. 페이지 새로고침 (Cmd+R)
2. Extension 재활성화
3. Chrome 재시작
```

### ❌ "Manifest 파일을 로드할 수 없습니다"
```bash
# 원인: 잘못된 폴더 선택
# 해결: chrome-extension 폴더를 정확히 선택
```

---

## 📝 수동 설치 명령어 (터미널)

```bash
# 1. Extension 폴더로 이동
cd /Users/david/Documents/Audio-Video/image-to-video-mac/chrome-extension

# 2. 파일 확인
ls -la
# 다음 파일들이 있어야 함:
# - manifest.json
# - content.js
# - popup.html
# - background.js
# - style.css

# 3. Chrome에서 폴더 경로 복사
pwd
# 출력된 경로를 복사하여 Chrome에서 사용
```

---

## 🎨 Extension 구조

```
chrome-extension/
├── manifest.json      # Extension 설정 파일 (필수)
├── content.js         # 웹 페이지에 주입되는 스크립트
├── background.js      # 백그라운드 서비스 워커
├── popup.html         # 팝업 UI
├── popup.js           # 팝업 스크립트
├── style.css          # 스타일시트
├── icon-16.png        # 아이콘 (16x16)
├── icon-48.png        # 아이콘 (48x48)
└── icon-128.png       # 아이콘 (128x128)
```

---

## ⚡ 빠른 설치 체크리스트

- [ ] Chrome 브라우저 실행
- [ ] chrome://extensions/ 접속
- [ ] 개발자 모드 ON
- [ ] "압축 해제된 확장 프로그램 로드" 클릭
- [ ] chrome-extension 폴더 선택
- [ ] Extension 목록에 표시 확인
- [ ] 브라우저 상단에 아이콘 고정
- [ ] Discord/Midjourney 사이트 접속
- [ ] 우측 하단 플로팅 버튼 확인

---

## 🔒 보안 및 권한

Extension이 요청하는 권한:
- **activeTab**: 현재 탭 접근
- **storage**: 설정 및 이미지 정보 저장
- **downloads**: 이미지 다운로드
- **host_permissions**: Discord, Midjourney, localhost 접근

---

## 📞 지원

문제가 계속되면:
1. Chrome 버전 확인 (최신 버전 권장)
2. 콘솔 로그 확인 (F12 → Console)
3. Extension 재설치

---

✨ **설치 완료!** 이제 Midjourney 이미지를 자동으로 수집하고 동영상으로 만들 수 있습니다!