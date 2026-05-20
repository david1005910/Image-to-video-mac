# 🎬 Image to Video - Mac용 이미지 동영상 변환기

이미지를 업로드하면 자동으로 동영상을 생성하는 Remotion 기반 앱입니다.

## 🚀 빠른 시작

### 1. Redis 설치 및 실행
```bash
brew install redis
brew services start redis
```

### 2. 프로젝트 설정
```bash
npm run setup
```

### 3. 실행
```bash
npm start
```

### 4. 브라우저에서 접속
```
http://localhost:3000
```

## 🎯 사용 방법

1. 이미지 파일들 선택 (여러 개 가능)
2. 스타일 선택:
   - **슬라이드쇼**: 부드러운 페이드
   - **켄번즈**: 다큐멘터리 스타일 줌/팬
   - **콜라주**: 슬라이드 인 애니메이션
3. 렌더링 시작
4. 완료 후 다운로드

## 🛠 트러블슈팅

### Redis 연결 오류
```bash
brew services restart redis
```

### 포트 충돌
.env 파일에서 PORT 변경

### Sharp 오류 (M1/M2 Mac)
```bash
arch -x86_64 npm install sharp
```

## 💡 팁

- 권장 이미지 크기: 1920x1080
- 지원 형식: JPG, PNG, WebP, GIF
- 렌더링 시간: 이미지 10개당 약 2-5분

---

Made with ❤️ using Remotion
