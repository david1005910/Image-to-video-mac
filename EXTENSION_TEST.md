# 🧪 Chrome Extension 테스트 가이드

## 1️⃣ Extension 설치/재로드

### Chrome에서:
1. 주소창에 입력: `chrome://extensions/`
2. 우측 상단 "개발자 모드" ON
3. 기존 Extension이 있다면:
   - 새로고침 버튼(↻) 클릭
4. 없다면:
   - "압축 해제된 확장 프로그램 로드" 클릭
   - 폴더 선택: `/Users/david/Documents/Audio-Video/image-to-video-mac/chrome-extension`

---

## 2️⃣ 테스트 순서

### A. 기본 기능 테스트
1. **Extension 팝업 열기**
   - 브라우저 우측 상단 🎬 아이콘 클릭
   - 팝업 창이 열리는지 확인

2. **이미지 파일 업로드**
   - "📁 이미지 파일 업로드" 클릭
   - 이미지 선택
   - 그리드에 표시되는지 확인

3. **AI 이미지 생성**
   - "🎨 AI 이미지 생성" 클릭
   - 프롬프트 입력: "beautiful sunset"
   - "🚀 생성 시작" 클릭
   - 10-20초 대기

### B. 삭제 기능 테스트
1. 이미지 위에 마우스 올리기
2. 우측 상단 × 버튼 클릭
3. 확인 다이얼로그에서 "확인"
4. 이미지가 삭제되는지 확인

### C. Colab 연동 테스트
1. **"Colab에서 편집" 클릭**
   - Drive 업로드 패널 열림
   - Session ID 생성 확인

2. **Session ID 복사**
   - Session ID 클릭
   - "복사됨!" 메시지 확인

3. **Drive 업로드** (OAuth 설정 필요)
   - "📤 Drive 업로드 시작" 클릭
   - Google 로그인
   - 업로드 진행 상태 확인

---

## 3️⃣ 디버깅

### 콘솔 로그 확인
1. Extension 팝업에서 우클릭
2. "검사" 선택
3. Console 탭에서 로그 확인

### 주요 확인 사항:
```javascript
// 이미지 수 확인
console.log(document.getElementById('imageCount').textContent)

// Storage 확인
chrome.storage.local.get(['mjvc_images'], (result) => {
  console.log('저장된 이미지:', result.mjvc_images)
})

// Session ID 확인  
console.log(document.getElementById('sessionId').textContent)
```

---

## 4️⃣ 테스트 체크리스트

- [ ] Extension 아이콘 표시
- [ ] 팝업 창 열기
- [ ] 이미지 파일 업로드
- [ ] AI 이미지 생성 (Pollinations)
- [ ] 이미지 개별 삭제
- [ ] 전체 초기화
- [ ] Colab 연동 패널
- [ ] Session ID 생성/복사
- [ ] 탭 전환 (메인/설정/가이드)
- [ ] 설정 저장

---

## 5️⃣ 알려진 이슈

### OAuth2 설정 필요
Google Drive 업로드를 위해서는:
1. Google Cloud Console에서 프로젝트 생성
2. OAuth2 Client ID 발급
3. manifest.json에 Client ID 추가

### CORS 에러
Pollinations API 호출 시 CORS 에러가 발생할 수 있음
→ Extension 환경에서는 정상 작동

### 메모리 제한
너무 많은 이미지(100개 이상) 저장 시 속도 저하
→ 주기적으로 초기화 권장

---

## 6️⃣ 빠른 테스트 명령

```bash
# Extension 폴더로 이동
cd /Users/david/Documents/Audio-Video/image-to-video-mac/chrome-extension

# 파일 확인
ls -la *.json *.js *.html

# 테스트 페이지 열기
open test-page.html

# 로컬 서버 실행 (필요시)
cd ..
npm run dev
```

---

*테스트 완료 후 문제가 있으면 알려주세요!*