// Midjourney 이미지 수집 및 동영상 생성 Content Script

class MidjourneyVideoCreator {
  constructor() {
    this.images = [];
    this.observer = null;
    this.isCollecting = false;
    this.init();
  }

  init() {
    // 페이지 로드 완료 후 실행
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.setup());
    } else {
      this.setup();
    }
  }

  setup() {
    // Floating 버튼 생성
    this.createFloatingButton();
    
    // 이미지 감지 시작
    this.startImageDetection();
    
    // 메시지 리스너 등록
    this.setupMessageListener();
  }

  createFloatingButton() {
    const button = document.createElement('div');
    button.id = 'mj-video-creator-btn';
    button.innerHTML = `
      <div class="mj-vc-container">
        <button class="mj-vc-main-btn">🎬</button>
        <div class="mj-vc-panel" style="display: none;">
          <h3>Midjourney Video Creator</h3>
          <div class="mj-vc-status">
            수집된 이미지: <span id="mj-vc-count">0</span>개
          </div>
          <div class="mj-vc-controls">
            <button id="mj-vc-collect">📸 이미지 수집 시작</button>
            <button id="mj-vc-stop" style="display: none;">⏹ 수집 중지</button>
            <button id="mj-vc-create">🎬 동영상 생성</button>
            <button id="mj-vc-clear">🗑️ 초기화</button>
          </div>
          <div class="mj-vc-options">
            <label>
              <input type="checkbox" id="mj-vc-auto"> 자동 수집
            </label>
            <label>
              <input type="checkbox" id="mj-vc-upscale" checked> Upscale만 수집
            </label>
          </div>
          <div id="mj-vc-preview" class="mj-vc-preview"></div>
        </div>
      </div>
    `;
    document.body.appendChild(button);

    // 이벤트 리스너 등록
    this.setupButtonEvents(button);
  }

  setupButtonEvents(button) {
    const mainBtn = button.querySelector('.mj-vc-main-btn');
    const panel = button.querySelector('.mj-vc-panel');
    const collectBtn = button.querySelector('#mj-vc-collect');
    const stopBtn = button.querySelector('#mj-vc-stop');
    const createBtn = button.querySelector('#mj-vc-create');
    const clearBtn = button.querySelector('#mj-vc-clear');
    const autoCheck = button.querySelector('#mj-vc-auto');

    mainBtn.addEventListener('click', () => {
      panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
    });

    collectBtn.addEventListener('click', () => {
      this.startCollecting();
      collectBtn.style.display = 'none';
      stopBtn.style.display = 'block';
    });

    stopBtn.addEventListener('click', () => {
      this.stopCollecting();
      collectBtn.style.display = 'block';
      stopBtn.style.display = 'none';
    });

    createBtn.addEventListener('click', () => {
      this.createVideo();
    });

    clearBtn.addEventListener('click', () => {
      this.clearImages();
    });

    autoCheck.addEventListener('change', (e) => {
      if (e.target.checked) {
        this.startAutoCollection();
      } else {
        this.stopAutoCollection();
      }
    });
  }

  startImageDetection() {
    // Discord의 경우
    if (window.location.hostname === 'discord.com') {
      this.detectDiscordImages();
    }
    // Midjourney 웹사이트의 경우
    else if (window.location.hostname === 'www.midjourney.com') {
      this.detectMidjourneyWebImages();
    }
  }

  detectDiscordImages() {
    // Discord에서 Midjourney 이미지 감지
    this.observer = new MutationObserver((mutations) => {
      if (!this.isCollecting) return;

      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === 1) { // Element node
            // Midjourney 이미지 찾기
            const images = node.querySelectorAll('img[src*="cdn.midjourney.com"], img[src*="media.discordapp.net"]');
            images.forEach(img => this.collectImage(img));

            // 메시지 내 이미지 링크 찾기
            const links = node.querySelectorAll('a[href*="cdn.midjourney.com"], a[href*="media.discordapp.net"]');
            links.forEach(link => {
              if (link.href.match(/\.(png|jpg|jpeg|webp)/i)) {
                this.collectImageUrl(link.href);
              }
            });
          }
        });
      });
    });

    // Discord 채팅 영역 감시
    const chatArea = document.querySelector('[class*="chat"]') || document.body;
    this.observer.observe(chatArea, {
      childList: true,
      subtree: true
    });
  }

  detectMidjourneyWebImages() {
    // Midjourney 웹사이트에서 이미지 감지
    this.observer = new MutationObserver((mutations) => {
      if (!this.isCollecting) return;

      const images = document.querySelectorAll('img[src*="cdn.midjourney.com"]');
      images.forEach(img => this.collectImage(img));
    });

    this.observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  }

  collectImage(img) {
    const src = img.src;
    
    // 중복 체크
    if (this.images.some(i => i.url === src)) return;
    
    // Upscale 이미지만 수집 옵션 체크
    const upscaleOnly = document.querySelector('#mj-vc-upscale')?.checked;
    if (upscaleOnly && !this.isUpscaledImage(src)) return;

    // 이미지 정보 수집
    const imageData = {
      url: src,
      timestamp: Date.now(),
      title: this.extractPromptFromImage(img),
      width: img.naturalWidth || img.width,
      height: img.naturalHeight || img.height
    };

    this.images.push(imageData);
    this.updateUI();
    this.saveToStorage();
  }

  collectImageUrl(url) {
    if (this.images.some(i => i.url === url)) return;

    const imageData = {
      url: url,
      timestamp: Date.now(),
      title: `Image ${this.images.length + 1}`
    };

    this.images.push(imageData);
    this.updateUI();
    this.saveToStorage();
  }

  isUpscaledImage(url) {
    // Upscale된 이미지 판별 (일반적으로 더 큰 해상도)
    return url.includes('_upscaled') || 
           url.includes('U1') || url.includes('U2') || 
           url.includes('U3') || url.includes('U4') ||
           !url.includes('grid');
  }

  extractPromptFromImage(img) {
    // 이미지 주변의 프롬프트 텍스트 추출
    const parent = img.closest('[class*="message"]') || img.parentElement;
    if (parent) {
      const textElements = parent.querySelectorAll('[class*="text"], [class*="content"]');
      for (let el of textElements) {
        const text = el.textContent;
        if (text && text.length > 10 && !text.includes('Midjourney Bot')) {
          return text.substring(0, 100);
        }
      }
    }
    return `Image ${this.images.length + 1}`;
  }

  startCollecting() {
    this.isCollecting = true;
    this.showNotification('이미지 수집을 시작합니다');
    
    // 현재 페이지의 모든 이미지 수집
    this.collectExistingImages();
  }

  stopCollecting() {
    this.isCollecting = false;
    this.showNotification('이미지 수집을 중지했습니다');
  }

  collectExistingImages() {
    // 현재 페이지의 모든 Midjourney 이미지 수집
    const images = document.querySelectorAll('img[src*="cdn.midjourney.com"], img[src*="media.discordapp.net"]');
    images.forEach(img => this.collectImage(img));
  }

  startAutoCollection() {
    this.isCollecting = true;
    this.autoScrollInterval = setInterval(() => {
      // 자동 스크롤하며 이미지 수집
      window.scrollBy(0, 500);
      
      // 페이지 끝 도달 체크
      if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 100) {
        clearInterval(this.autoScrollInterval);
        this.stopCollecting();
        this.showNotification('페이지 끝에 도달했습니다');
      }
    }, 2000);
  }

  stopAutoCollection() {
    if (this.autoScrollInterval) {
      clearInterval(this.autoScrollInterval);
    }
    this.stopCollecting();
  }

  async createVideo() {
    if (this.images.length === 0) {
      this.showNotification('수집된 이미지가 없습니다', 'error');
      return;
    }

    this.showNotification(`${this.images.length}개 이미지로 동영상 생성 중...`);

    try {
      // 이미지 다운로드 및 처리
      const imageBlobs = await this.downloadImages();
      
      // FormData 생성
      const formData = new FormData();
      formData.append('title', `Midjourney Video ${new Date().toLocaleString()}`);
      formData.append('style', 'kenburns');
      formData.append('duration', '3');
      formData.append('transition', 'zoom');
      formData.append('colorEffect', 'film');
      formData.append('motionEffect', 'kenburns');
      
      // 이미지 추가
      imageBlobs.forEach((blob, index) => {
        formData.append('images', blob, `image_${index}.jpg`);
      });

      // 로컬 서버로 전송
      const response = await fetch('http://localhost:3000/api/upload', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('업로드 실패');
      }

      const data = await response.json();
      
      // 렌더링 시작
      const renderResponse = await fetch(`http://localhost:3000/api/video/${data.videoId}/render`, {
        method: 'POST'
      });

      if (!renderResponse.ok) {
        throw new Error('렌더링 시작 실패');
      }

      this.showNotification('동영상 생성이 시작되었습니다! Video ID: ' + data.videoId, 'success');
      
      // 상태 체크
      this.checkVideoStatus(data.videoId);

    } catch (error) {
      console.error('Video creation error:', error);
      this.showNotification('동영상 생성 실패: ' + error.message, 'error');
    }
  }

  async downloadImages() {
    const blobs = [];
    
    for (let imageData of this.images) {
      try {
        const response = await fetch(imageData.url);
        const blob = await response.blob();
        blobs.push(blob);
      } catch (error) {
        console.error('Image download failed:', imageData.url, error);
      }
    }
    
    return blobs;
  }

  async checkVideoStatus(videoId) {
    let attempts = 0;
    const maxAttempts = 60; // 최대 3분 대기

    const interval = setInterval(async () => {
      attempts++;
      
      try {
        const response = await fetch(`http://localhost:3000/api/video/${videoId}`);
        const video = await response.json();
        
        if (video.status === 'completed') {
          clearInterval(interval);
          this.showNotification('동영상 생성 완료!', 'success');
          
          // 다운로드 링크 생성
          const downloadUrl = `http://localhost:3000/output/${videoId}.mp4`;
          this.createDownloadLink(downloadUrl);
          
        } else if (video.status === 'failed') {
          clearInterval(interval);
          this.showNotification('동영상 생성 실패', 'error');
        }
        
        if (attempts >= maxAttempts) {
          clearInterval(interval);
          this.showNotification('시간 초과', 'error');
        }
      } catch (error) {
        console.error('Status check failed:', error);
      }
    }, 3000);
  }

  createDownloadLink(url) {
    const panel = document.querySelector('.mj-vc-panel');
    const downloadDiv = document.createElement('div');
    downloadDiv.className = 'mj-vc-download';
    downloadDiv.innerHTML = `
      <a href="${url}" download target="_blank" class="mj-vc-download-btn">
        📥 동영상 다운로드
      </a>
    `;
    panel.appendChild(downloadDiv);
  }

  clearImages() {
    this.images = [];
    this.updateUI();
    this.saveToStorage();
    this.showNotification('이미지 목록을 초기화했습니다');
  }

  updateUI() {
    // 이미지 개수 업데이트
    const countEl = document.querySelector('#mj-vc-count');
    if (countEl) {
      countEl.textContent = this.images.length;
    }

    // 미리보기 업데이트
    const previewEl = document.querySelector('#mj-vc-preview');
    if (previewEl) {
      previewEl.innerHTML = '';
      this.images.slice(-6).forEach(img => {
        const imgEl = document.createElement('img');
        imgEl.src = img.url;
        imgEl.style.width = '60px';
        imgEl.style.height = '60px';
        imgEl.style.objectFit = 'cover';
        imgEl.style.margin = '2px';
        imgEl.style.borderRadius = '4px';
        previewEl.appendChild(imgEl);
      });
    }
  }

  saveToStorage() {
    // Chrome storage에 저장
    chrome.storage.local.set({ 
      'mjvc_images': this.images 
    });
  }

  loadFromStorage() {
    chrome.storage.local.get(['mjvc_images'], (result) => {
      if (result.mjvc_images) {
        this.images = result.mjvc_images;
        this.updateUI();
      }
    });
  }

  setupMessageListener() {
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.action === 'getImages') {
        sendResponse({ images: this.images });
      } else if (request.action === 'clearImages') {
        this.clearImages();
        sendResponse({ success: true });
      }
    });
  }

  showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `mj-vc-notification mj-vc-notification-${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.remove();
    }, 3000);
  }
}

// 초기화
const mjVideoCreator = new MidjourneyVideoCreator();