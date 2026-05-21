// Popup script for Chrome Extension

document.addEventListener('DOMContentLoaded', function() {
  // 탭 전환
  const tabs = document.querySelectorAll('.tab');
  const tabContents = document.querySelectorAll('.tab-content');
  
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetTab = tab.dataset.tab;
      
      tabs.forEach(t => t.classList.remove('active'));
      tabContents.forEach(tc => tc.classList.remove('active'));
      
      tab.classList.add('active');
      document.getElementById(targetTab).classList.add('active');
    });
  });

  // 이미지 수 및 상태 업데이트
  updateImageCount();
  
  // 버튼 이벤트
  document.getElementById('startCollect').addEventListener('click', () => {
    sendMessageToContent({ action: 'startCollect' });
    document.getElementById('startCollect').style.display = 'none';
    document.getElementById('stopCollect').style.display = 'block';
    updateStatus('수집 중...');
  });
  
  document.getElementById('stopCollect').addEventListener('click', () => {
    sendMessageToContent({ action: 'stopCollect' });
    document.getElementById('startCollect').style.display = 'block';
    document.getElementById('stopCollect').style.display = 'none';
    updateStatus('수집 중지됨');
  });
  
  document.getElementById('createVideo').addEventListener('click', () => {
    sendMessageToContent({ action: 'createVideo' });
    updateStatus('동영상 생성 중...');
  });
  
  document.getElementById('clearImages').addEventListener('click', () => {
    if (confirm('수집된 모든 이미지를 삭제하시겠습니까?')) {
      sendMessageToContent({ action: 'clearImages' });
      updateImageCount();
      updateStatus('초기화됨');
    }
  });
  
  document.getElementById('openTab').addEventListener('click', () => {
    chrome.tabs.create({ url: 'https://discord.com/channels/@me' });
  });
  
  // AI 이미지 생성 패널 토글
  const generateBtn = document.getElementById('generateBtn');
  const generatePanel = document.getElementById('generatePanel');
  const cancelGenerate = document.getElementById('cancelGenerate');
  const doGenerate = document.getElementById('doGenerate');
  const promptInput = document.getElementById('promptInput');
  const imageModel = document.getElementById('imageModel');
  const imageWidth = document.getElementById('imageWidth');
  const imageHeight = document.getElementById('imageHeight');
  const generateStatus = document.getElementById('generateStatus');
  
  generateBtn.addEventListener('click', () => {
    generatePanel.style.display = generatePanel.style.display === 'none' ? 'block' : 'none';
    if (generatePanel.style.display === 'block') {
      promptInput.focus();
    }
  });
  
  cancelGenerate.addEventListener('click', () => {
    generatePanel.style.display = 'none';
    generateStatus.textContent = '';
  });
  
  // AI 이미지 생성 실행
  doGenerate.addEventListener('click', async () => {
    const prompt = promptInput.value.trim();
    if (!prompt) {
      generateStatus.textContent = '⚠️ 프롬프트를 입력해주세요';
      return;
    }
    
    generateStatus.textContent = '🎨 이미지 생성 중... (약 10-20초 소요)';
    doGenerate.disabled = true;
    
    try {
      // Pollinations API URL 생성
      const model = imageModel.value;
      const width = imageWidth.value || 1024;
      const height = imageHeight.value || 1024;
      const seed = Math.floor(Math.random() * 1000000);
      
      // URL 인코딩
      const encodedPrompt = encodeURIComponent(prompt);
      
      // Pollinations API 엔드포인트
      let imageUrl;
      if (model === 'any') {
        // 모델 자동 선택
        imageUrl = `https://image.pollinations.ai/prompt/${encodedPrompt}?width=${width}&height=${height}&seed=${seed}&nologo=true`;
      } else {
        // 특정 모델 사용
        imageUrl = `https://image.pollinations.ai/prompt/${encodedPrompt}?model=${model}&width=${width}&height=${height}&seed=${seed}&nologo=true`;
      }
      
      console.log('Generating image with URL:', imageUrl);
      
      // 이미지 로드 대기
      const img = new Image();
      img.crossOrigin = 'anonymous';
      
      await new Promise((resolve, reject) => {
        img.onload = resolve;
        img.onerror = reject;
        img.src = imageUrl;
      });
      
      // Canvas를 사용해 Data URL로 변환
      const canvas = document.createElement('canvas');
      canvas.width = img.width;
      canvas.height = img.height;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0);
      
      const dataUrl = canvas.toDataURL('image/png');
      
      // 생성된 이미지를 컬렉션에 추가
      chrome.storage.local.get(['mjvc_images'], (result) => {
        const existingImages = result.mjvc_images || [];
        const newImage = {
          url: dataUrl,
          filename: `AI_${prompt.substring(0, 20)}_${Date.now()}.png`,
          timestamp: Date.now(),
          type: 'generated',
          prompt: prompt,
          model: model
        };
        
        const allImages = [...existingImages, newImage];
        chrome.storage.local.set({ 'mjvc_images': allImages }, () => {
          console.log('AI generated image saved');
          updateImageCount();
          generateStatus.textContent = '✅ 이미지 생성 성공!';
          promptInput.value = '';
          
          setTimeout(() => {
            generatePanel.style.display = 'none';
            generateStatus.textContent = '';
          }, 2000);
        });
      });
      
    } catch (error) {
      console.error('Image generation failed:', error);
      generateStatus.textContent = '❌ 생성 실패: ' + error.message;
    } finally {
      doGenerate.disabled = false;
    }
  });
  
  // Enter 키로 생성
  promptInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      doGenerate.click();
    }
  });
  
  // Google Drive / Colab 연동
  const uploadToDrive = document.getElementById('uploadToDrive');
  const driveUploadPanel = document.getElementById('driveUploadPanel');
  const closeDrivePanel = document.getElementById('closeDrivePanel');
  const doUploadDrive = document.getElementById('doUploadDrive');
  const openColab = document.getElementById('openColab');
  const driveStatus = document.getElementById('driveStatus');
  const sessionId = document.getElementById('sessionId');
  const uploadProgress = document.getElementById('uploadProgress');
  
  // Session ID 생성
  function generateSessionId() {
    return 'session_' + Math.random().toString(36).substr(2, 9);
  }
  
  uploadToDrive.addEventListener('click', () => {
    driveUploadPanel.style.display = driveUploadPanel.style.display === 'none' ? 'block' : 'none';
    
    if (driveUploadPanel.style.display === 'block') {
      // 세션 ID 생성
      const sid = generateSessionId();
      sessionId.textContent = sid;
      sessionId.style.cursor = 'pointer';
      sessionId.title = '클릭하여 복사';
      
      // 클릭 시 복사
      sessionId.addEventListener('click', () => {
        navigator.clipboard.writeText(sid);
        const orig = sessionId.textContent;
        sessionId.textContent = '복사됨!';
        setTimeout(() => { sessionId.textContent = orig; }, 1000);
      });
      
      driveStatus.innerHTML = '<span>✅ 연동 준비 완료</span>';
      driveStatus.className = 'drive-status success';
    }
  });
  
  closeDrivePanel.addEventListener('click', () => {
    driveUploadPanel.style.display = 'none';
  });
  
  // Google Drive 업로드 (대체 방법: JSON 다운로드)
  doUploadDrive.addEventListener('click', async () => {
    driveStatus.innerHTML = '<span>🔄 업로드 중...</span>';
    driveStatus.className = 'drive-status uploading';
    
    // 이미지 데이터 가져오기
    chrome.storage.local.get(['mjvc_images'], async (result) => {
      const images = result.mjvc_images || [];
      
      if (images.length === 0) {
        driveStatus.innerHTML = '<span>⚠️ 업로드할 이미지가 없습니다</span>';
        driveStatus.className = 'drive-status error';
        return;
      }
      
      try {
        // OAuth2 설정이 없으므로 JSON 파일로 다운로드
        const exportData = {
          session_id: sessionId.textContent,
          created_at: new Date().toISOString(),
          image_count: images.length,
          images: images
        };
        
        // JSON 파일 생성
        const jsonBlob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(jsonBlob);
        
        // 다운로드 링크 생성
        chrome.downloads.download({
          url: url,
          filename: `midjourney_images_${sessionId.textContent}.json`,
          saveAs: true
        }, (downloadId) => {
          if (chrome.runtime.lastError) {
            driveStatus.innerHTML = '<span>❌ 다운로드 실패</span>';
            driveStatus.className = 'drive-status error';
            console.error(chrome.runtime.lastError);
          } else {
            driveStatus.innerHTML = '<span>✅ JSON 파일 다운로드 완료!</span>';
            driveStatus.className = 'drive-status success';
            
            uploadProgress.innerHTML = `
              <div style="font-size: 12px; color: #34a853;">
                <b>파일 다운로드 완료!</b><br>
                Session ID: ${sessionId.textContent}<br>
                이미지 수: ${images.length}개<br><br>
                <b>다음 단계:</b><br>
                1. 다운로드된 JSON 파일을 Google Drive에 업로드<br>
                2. Colab 노트북 열기<br>
                3. Session ID 입력 또는 JSON 파일 업로드<br>
                4. 영상 편집 실행
              </div>
            `;
          }
          URL.revokeObjectURL(url);
        });
        
        // 참고용 코드 (나중에 OAuth2 설정 시 사용)
        /*
        chrome.identity.getAuthToken({ interactive: true }, async (token) => {
          if (chrome.runtime.lastError || !token) {
            console.error('Auth error:', chrome.runtime.lastError);
            driveStatus.innerHTML = '<span>❌ Google 로그인 실패</span>';
            driveStatus.className = 'drive-status error';
            return;
          }
          
          // Drive 폴더 생성
          const folderName = `ChromeExtension_${sessionId.textContent}`;
          const folderResponse = await fetch('https://www.googleapis.com/drive/v3/files', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              name: folderName,
              mimeType: 'application/vnd.google-apps.folder'
            })
          });
          
          const folder = await folderResponse.json();
          const folderId = folder.id;
          
          // 이미지 업로드
          let uploaded = 0;
          uploadProgress.innerHTML = `<div style="font-size: 12px;">업로드: 0/${images.length}</div>`;
          
          // 메타데이터 JSON 생성
          const metadata = {
            session_id: sessionId.textContent,
            created_at: new Date().toISOString(),
            image_count: images.length,
            images: []
          };
          
          for (let img of images) {
            // Data URL을 Blob으로 변환
            let blob;
            if (img.url.startsWith('data:')) {
              const response = await fetch(img.url);
              blob = await response.blob();
            } else {
              // URL에서 다운로드
              const response = await fetch(img.url);
              blob = await response.blob();
            }
            
            // 이미지 메타데이터
            metadata.images.push({
              filename: img.filename || `image_${uploaded}.png`,
              timestamp: img.timestamp,
              type: img.type,
              prompt: img.prompt
            });
            
            uploaded++;
            uploadProgress.innerHTML = `<div style="font-size: 12px;">업로드: ${uploaded}/${images.length}</div>`;
          }
          
          // 메타데이터 JSON 저장
          const jsonBlob = new Blob([JSON.stringify(metadata, null, 2)], { type: 'application/json' });
          const jsonForm = new FormData();
          jsonForm.append('metadata', JSON.stringify({
            name: 'images.json',
            parents: [folderId]
          }));
          jsonForm.append('file', jsonBlob);
          
          await fetch('https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`
            },
            body: jsonForm
          });
          
          driveStatus.innerHTML = '<span>✅ 업로드 완료!</span>';
          driveStatus.className = 'drive-status success';
          uploadProgress.innerHTML = `<div style="font-size: 12px; color: #34a853;">
            폴더: ${folderName}<br>
            이미지: ${images.length}개<br>
            Colab에서 Session ID를 입력하세요
          </div>`;
        });
        */
        
      } catch (error) {
        console.error('Upload error:', error);
        driveStatus.innerHTML = '<span>❌ 업로드 실패</span>';
        driveStatus.className = 'drive-status error';
      }
    });
  });
  
  // Colab 노트북 열기
  openColab.addEventListener('click', () => {
    // Colab 노트북 파일을 Google Drive에 업로드하거나 GitHub에 호스팅 필요
    // 임시로 로컬 파일 경로 사용
    const colabInfo = `
      <div style="font-size: 12px; padding: 10px; background: rgba(249,171,0,0.2); border-radius: 6px; margin-top: 10px;">
        <b>📓 Colab 노트북 사용법:</b><br><br>
        1. <a href="https://colab.research.google.com" target="_blank">Google Colab</a> 열기<br>
        2. 파일 → 노트북 업로드<br>
        3. colab_video_editor.ipynb 선택<br>
        4. 위에서 다운로드한 JSON 파일 업로드<br>
        5. Session ID: <code>${sessionId.textContent}</code> 입력<br>
      </div>
    `;
    uploadProgress.innerHTML = colabInfo;
    
    // Colab 페이지 열기
    chrome.tabs.create({ url: 'https://colab.research.google.com' });
  });
  
  // 업로드 버튼 클릭 처리
  document.getElementById('uploadBtn').addEventListener('click', () => {
    document.getElementById('fileInput').click();
  });
  
  // 파일 업로드 처리
  const fileInput = document.getElementById('fileInput');
  if (fileInput) {
    fileInput.addEventListener('change', async (event) => {
      console.log('File input change event triggered');
      const files = event.target.files;
      if (files && files.length > 0) {
        console.log(`Processing ${files.length} files`);
        updateStatus(`${files.length}개 파일 처리 중...`);
        
        try {
          // 파일을 Data URL로 변환
          const newImages = [];
          for (let i = 0; i < files.length; i++) {
            const file = files[i];
            console.log(`Processing file: ${file.name}, type: ${file.type}`);
            
            if (file.type.startsWith('image/')) {
              try {
                const dataUrl = await fileToDataUrl(file);
                console.log(`File converted to Data URL: ${file.name}`);
                newImages.push({
                  url: dataUrl,
                  filename: file.name,
                  timestamp: Date.now(),
                  type: 'uploaded'
                });
              } catch (error) {
                console.error(`파일 변환 실패 ${file.name}:`, error);
              }
            } else {
              console.log(`Skipping non-image file: ${file.name}`);
            }
          }
          
          if (newImages.length > 0) {
            // 기존 이미지 목록 가져오기
            chrome.storage.local.get(['mjvc_images'], (result) => {
              const existingImages = result.mjvc_images || [];
              const allImages = [...existingImages, ...newImages];
              
              // 저장
              chrome.storage.local.set({ 'mjvc_images': allImages }, () => {
                console.log(`Saved ${newImages.length} new images to storage`);
                updateImageCount();
                updateStatus(`${newImages.length}개 이미지 추가됨`);
              });
            });
          } else {
            updateStatus('이미지 파일이 없습니다');
          }
          
          // 입력 초기화
          event.target.value = '';
        } catch (error) {
          console.error('File processing error:', error);
          updateStatus('파일 처리 중 오류 발생');
        }
      }
    });
  } else {
    console.error('File input element not found');
  }
  
  // 설정 저장
  const settings = ['autoCollect', 'upscaleOnly', 'autoScroll', 'videoStyle', 'duration', 'transition'];
  settings.forEach(id => {
    const element = document.getElementById(id);
    if (element) {
      // 저장된 설정 불러오기
      chrome.storage.local.get([id], (result) => {
        if (result[id] !== undefined) {
          if (element.type === 'checkbox') {
            element.checked = result[id];
          } else {
            element.value = result[id];
          }
        }
      });
      
      // 설정 변경 시 저장
      element.addEventListener('change', () => {
        const value = element.type === 'checkbox' ? element.checked : element.value;
        chrome.storage.local.set({ [id]: value });
      });
    }
  });
});

function sendMessageToContent(message) {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs[0]) {
      chrome.tabs.sendMessage(tabs[0].id, message, (response) => {
        if (response) {
          console.log('Response:', response);
          if (response.images) {
            updateImageGrid(response.images);
          }
        }
      });
    }
  });
}

function updateImageCount() {
  chrome.storage.local.get(['mjvc_images'], (result) => {
    const images = result.mjvc_images || [];
    document.getElementById('imageCount').textContent = images.length;
    updateImageGrid(images);
  });
}

function updateImageGrid(images) {
  const grid = document.getElementById('imageGrid');
  if (grid && images) {
    console.log(`Updating image grid with ${images.length} images`);
    grid.innerHTML = '';
    
    // 최근 8개 이미지만 표시 (역순으로)
    const displayImages = images.slice(-8).reverse();
    
    displayImages.forEach((img, displayIndex) => {
      // 실제 배열에서의 인덱스 찾기
      const actualIndex = images.length - 1 - displayIndex;
      
      // 컨테이너 생성
      const container = document.createElement('div');
      container.className = 'image-thumb-container';
      
      // 이미지 엘리먼트 생성
      const imgEl = document.createElement('img');
      imgEl.src = img.url;
      imgEl.className = 'image-thumb';
      imgEl.title = img.filename || `Image ${actualIndex + 1}`;
      imgEl.onerror = () => {
        console.error(`Failed to load image: ${img.filename || img.url.substring(0, 50)}`);
        container.style.display = 'none';
      };
      
      // 삭제 버튼 생성
      const deleteBtn = document.createElement('button');
      deleteBtn.className = 'delete-btn';
      deleteBtn.innerHTML = '×';
      deleteBtn.title = '이미지 삭제';
      deleteBtn.onclick = (e) => {
        e.stopPropagation();
        deleteImage(actualIndex);
      };
      
      container.appendChild(imgEl);
      container.appendChild(deleteBtn);
      grid.appendChild(container);
    });
  }
}

function updateStatus(status) {
  document.getElementById('status').textContent = status;
  document.getElementById('statusMessage').textContent = status;
}

// 파일을 Data URL로 변환하는 헬퍼 함수
function fileToDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => resolve(e.target.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

// 개별 이미지 삭제 함수
function deleteImage(index) {
  chrome.storage.local.get(['mjvc_images'], (result) => {
    const images = result.mjvc_images || [];
    
    if (index >= 0 && index < images.length) {
      const deletedImage = images[index];
      
      // 삭제 확인
      if (confirm(`이미지를 삭제하시겠습니까?\n${deletedImage.filename || 'Image ' + (index + 1)}`)) {
        // 배열에서 이미지 제거
        images.splice(index, 1);
        
        // 저장
        chrome.storage.local.set({ 'mjvc_images': images }, () => {
          console.log(`Deleted image at index ${index}`);
          updateImageCount();
          updateStatus(`이미지 삭제됨`);
          
          // Content script에도 알림
          sendMessageToContent({ action: 'imageDeleted', index: index });
        });
      }
    }
  });
}

// Pollinations API를 사용한 이미지 생성 함수 (대체 방법)
async function generateImageFromPollinations(prompt, options = {}) {
  const { model = 'flux', width = 1024, height = 1024 } = options;
  const seed = Math.floor(Math.random() * 1000000);
  const encodedPrompt = encodeURIComponent(prompt);
  
  let apiUrl;
  if (model === 'any') {
    apiUrl = `https://image.pollinations.ai/prompt/${encodedPrompt}?width=${width}&height=${height}&seed=${seed}&nologo=true`;
  } else {
    apiUrl = `https://image.pollinations.ai/prompt/${encodedPrompt}?model=${model}&width=${width}&height=${height}&seed=${seed}&nologo=true`;
  }
  
  // Fetch API를 사용한 직접 다운로드
  try {
    const response = await fetch(apiUrl);
    if (!response.ok) throw new Error('API 응답 실패');
    
    const blob = await response.blob();
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result);
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  } catch (error) {
    console.error('Pollinations API error:', error);
    throw error;
  }
}

// Google Drive API 헬퍼 (대체 방법)
async function uploadToGoogleDrive(images, sessionId) {
  // Chrome Extension에서는 OAuth2 토큰이 필요
  // manifest.json에 oauth2 권한 추가 필요:
  // "oauth2": {
  //   "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
  //   "scopes": ["https://www.googleapis.com/auth/drive.file"]
  // }
  
  return new Promise((resolve, reject) => {
    chrome.identity.getAuthToken({ interactive: true }, async (token) => {
      if (chrome.runtime.lastError || !token) {
        reject(chrome.runtime.lastError);
        return;
      }
      
      try {
        // Drive API로 파일 업로드
        // ... 업로드 로직 ...
        resolve({ success: true, folderId: 'folder_id' });
      } catch (error) {
        reject(error);
      }
    });
  });
}

// 주기적으로 이미지 수 업데이트
setInterval(updateImageCount, 2000);