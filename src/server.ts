import express from 'express';
import cors from 'cors';
import path from 'path';
import { uploadRouter } from './routes/upload';
import { videoRouter } from './routes/video';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use('/uploads', express.static(path.join(__dirname, '../public/uploads')));
app.use('/output', express.static(path.join(__dirname, '../public/output')));
app.use(express.static(path.join(__dirname, '../')));
app.use('/api/upload', uploadRouter);
app.use('/api/video', videoRouter);

app.get('/', (req, res) => {
  res.send(`<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Image to Video</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { 
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      padding: 20px;
    }
    .container {
      max-width: 800px;
      margin: 50px auto;
      background: white;
      border-radius: 20px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
      padding: 40px;
    }
    h1 { color: #333; margin-bottom: 10px; font-size: 32px; }
    .subtitle { color: #666; margin-bottom: 30px; font-size: 16px; }
    .form-group { margin: 20px 0; }
    label { display: block; margin-bottom: 8px; font-weight: 600; color: #333; }
    input, select { 
      padding: 12px; 
      width: 100%; 
      border: 2px solid #e0e0e0;
      border-radius: 8px; 
      font-size: 14px; 
      transition: border 0.3s;
    }
    input:focus, select:focus { outline: none; border-color: #667eea; }
    input[type="file"] { padding: 10px; cursor: pointer; }
    button { 
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white; 
      padding: 15px 30px; 
      border: none; 
      border-radius: 8px;
      cursor: pointer; 
      font-size: 16px; 
      font-weight: 600; 
      width: 100%;
      transition: transform 0.2s;
    }
    button:hover { 
      transform: translateY(-2px); 
      box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4); 
    }
    button:active { transform: translateY(0); }
    button:disabled {
      background: #ccc;
      cursor: not-allowed;
      transform: none;
    }
    #result { 
      margin-top: 30px; 
      padding: 20px; 
      background: #f8f9fa; 
      border-radius: 8px;
      border-left: 4px solid #667eea;
    }
    .success { color: #28a745; font-weight: 600; }
    .error { color: #dc3545; font-weight: 600; }
    .info { color: #17a2b8; }
    .download-btn {
      display: inline-block;
      background: #28a745;
      color: white;
      padding: 12px 24px;
      border-radius: 8px;
      margin-top: 15px;
      text-decoration: none;
      font-weight: 600;
    }
    .download-btn:hover { background: #218838; }
  </style>
</head>
<body>
  <div class="container">
    <h1>🎬 이미지를 동영상으로 변환</h1>
    <p class="subtitle">여러 이미지를 업로드하고 멋진 동영상을 만들어보세요</p>
    
    <form id="uploadForm" enctype="multipart/form-data">
      <div class="form-group">
        <label>📝 비디오 제목</label>
        <input type="text" name="title" value="My Video" required>
      </div>
      
      <div class="form-group">
        <label>🖼️ 이미지 파일들 (여러 개 선택 가능)</label>
        <input type="file" name="images" multiple accept="image/*" required>
      </div>
      
      <div class="form-group">
        <label>🎨 스타일</label>
        <select name="style">
          <option value="slideshow">슬라이드쇼 (기본 페이드)</option>
          <option value="kenburns">켄번즈 효과 (줌/팬)</option>
          <option value="collage">콜라주 (슬라이드 인)</option>
        </select>
      </div>
      
      <div class="form-group">
        <label>⏱️ 이미지당 표시 시간 (초)</label>
        <input type="number" name="duration" value="3" min="1" max="10">
      </div>
      
      <div class="form-group">
        <label>✨ 트랜지션 효과</label>
        <select name="transition">
          <option value="fade">페이드</option>
          <option value="slide">슬라이드</option>
          <option value="zoom">줌</option>
          <option value="rotate">회전</option>
          <option value="blur">블러</option>
          <option value="dissolve">디졸브</option>
          <option value="wipe">와이프</option>
          <option value="none">없음</option>
        </select>
      </div>
      
      <div class="form-group">
        <label>🎨 색상 효과</label>
        <select name="colorEffect">
          <option value="">없음</option>
          <option value="sepia">세피아</option>
          <option value="grayscale">흑백</option>
          <option value="vintage">빈티지</option>
          <option value="bright">밝게</option>
          <option value="dark">어둡게</option>
          <option value="warm">따뜻한 톤</option>
          <option value="cold">차가운 톤</option>
          <option value="film">필름</option>
        </select>
      </div>
      
      <div class="form-group">
        <label>🎬 모션 효과</label>
        <select name="motionEffect">
          <option value="">없음</option>
          <option value="kenburns">켄번즈 (줌&팬)</option>
          <option value="shake">흔들림</option>
          <option value="pulse">펄스</option>
          <option value="drift">표류</option>
        </select>
      </div>
      
      <div class="form-group">
        <label>🖼️ 프레임 효과</label>
        <select name="frameEffect">
          <option value="">없음</option>
          <option value="vignette">비네트</option>
          <option value="border">테두리</option>
          <option value="rounded">둥근 모서리</option>
          <option value="polaroid">폴라로이드</option>
        </select>
      </div>
      
      <div class="form-group">
        <label>🎵 배경 음악 (선택)</label>
        <input type="file" name="music" accept="audio/*">
      </div>
      
      <div class="form-group">
        <label>📝 이미지별 캡션 (쉼표로 구분)</label>
        <input type="text" name="captions" placeholder="첫번째 이미지, 두번째 이미지, ...">
      </div>
      
      <div class="form-group">
        <label>📍 텍스트 위치</label>
        <select name="textPosition">
          <option value="bottom">하단 중앙</option>
          <option value="top">상단 중앙</option>
          <option value="center">중앙</option>
          <option value="bottom-left">하단 좌측</option>
          <option value="bottom-right">하단 우측</option>
        </select>
      </div>
      
      <button type="submit" id="submitBtn">🚀 업로드 & 렌더링 시작</button>
    </form>
    
    <div id="result" style="display:none;"></div>
  </div>
  
  <script>
    const form = document.getElementById('uploadForm');
    const submitBtn = document.getElementById('submitBtn');
    const resultDiv = document.getElementById('result');
    
    form.onsubmit = async (e) => {
      e.preventDefault();
      const formData = new FormData(e.target);
      
      submitBtn.disabled = true;
      submitBtn.textContent = '⏳ 처리 중...';
      resultDiv.style.display = 'block';
      resultDiv.innerHTML = '<p class="info">⏳ 이미지 업로드 중...</p>';
      
      try {
        const uploadRes = await fetch('/api/upload', {
          method: 'POST',
          body: formData
        });
        const uploadData = await uploadRes.json();
        
        if (!uploadRes.ok) throw new Error(uploadData.error);
        
        resultDiv.innerHTML = '<p class="info">⏳ 렌더링 큐에 추가 중...</p>';
        
        const renderRes = await fetch(\`/api/video/\${uploadData.videoId}/render\`, {
          method: 'POST'
        });
        
        if (!renderRes.ok) throw new Error('렌더링 시작 실패');
        
        resultDiv.innerHTML = \`
          <p class="success">✅ 렌더링이 시작되었습니다!</p>
          <p style="margin-top: 10px;">Video ID: <code>\${uploadData.videoId}</code></p>
          <p style="margin-top: 10px;">업로드된 이미지: <strong>\${uploadData.imageCount}개</strong></p>
        \`;
        
        let pollCount = 0;
        const interval = setInterval(async () => {
          pollCount++;
          try {
            const statusRes = await fetch(\`/api/video/\${uploadData.videoId}\`);
            const video = await statusRes.json();
            
            if (video.status === 'completed') {
              clearInterval(interval);
              submitBtn.disabled = false;
              submitBtn.textContent = '🚀 업로드 & 렌더링 시작';
              resultDiv.innerHTML = \`
                <p class="success">✅ 렌더링 완료!</p>
                <a href="/output/\${uploadData.videoId}.mp4" download class="download-btn">
                  📥 동영상 다운로드
                </a>
              \`;
            } else if (video.status === 'failed') {
              clearInterval(interval);
              submitBtn.disabled = false;
              submitBtn.textContent = '🚀 업로드 & 렌더링 시작';
              resultDiv.innerHTML = '<p class="error">❌ 렌더링 실패.</p>';
            } else {
              resultDiv.innerHTML = \`
                <p class="info">⏳ 렌더링 중... (상태: \${video.status})</p>
                <p style="margin-top: 5px; font-size: 14px; color: #666;">예상 시간: 2-5분</p>
              \`;
            }
            
            if (pollCount > 200) {
              clearInterval(interval);
              submitBtn.disabled = false;
              submitBtn.textContent = '🚀 업로드 & 렌더링 시작';
            }
          } catch (err) {
            console.error('Poll error:', err);
          }
        }, 3000);
        
      } catch (err) {
        submitBtn.disabled = false;
        submitBtn.textContent = '🚀 업로드 & 렌더링 시작';
        resultDiv.innerHTML = \`<p class="error">❌ 오류: \${err.message}</p>\`;
      }
    };
  </script>
</body>
</html>`);
});

app.listen(PORT, () => {
  console.log(`
  ╔═══════════════════════════════════════════╗
  ║   🎬 Image to Video Server Running       ║
  ║                                           ║
  ║   URL: http://localhost:${PORT}            ║
  ║                                           ║
  ║   브라우저에서 위 URL을 열어주세요       ║
  ╚═══════════════════════════════════════════╝
  `);
});
