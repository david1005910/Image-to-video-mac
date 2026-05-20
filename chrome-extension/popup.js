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
    grid.innerHTML = '';
    images.slice(-8).forEach(img => {
      const imgEl = document.createElement('img');
      imgEl.src = img.url;
      imgEl.className = 'image-thumb';
      grid.appendChild(imgEl);
    });
  }
}

function updateStatus(status) {
  document.getElementById('status').textContent = status;
  document.getElementById('statusMessage').textContent = status;
}

// 주기적으로 이미지 수 업데이트
setInterval(updateImageCount, 2000);