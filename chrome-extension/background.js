// Background service worker for Chrome Extension

// Extension 설치 시
chrome.runtime.onInstalled.addListener(() => {
  console.log('Midjourney Video Creator Extension 설치됨');
  
  // 초기 설정
  chrome.storage.local.set({
    autoCollect: true,
    upscaleOnly: true,
    autoScroll: false,
    videoStyle: 'kenburns',
    duration: 3,
    transition: 'zoom'
  });
});

// 메시지 리스너
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'downloadImage') {
    // 이미지 다운로드 처리
    chrome.downloads.download({
      url: request.url,
      filename: request.filename
    }, (downloadId) => {
      sendResponse({ success: true, downloadId });
    });
    return true;
  }
});

// 탭 업데이트 감지
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete') {
    // Discord 또는 Midjourney 사이트인 경우
    if (tab.url && (tab.url.includes('discord.com') || tab.url.includes('midjourney.com'))) {
      // Content script 주입 확인
      chrome.tabs.sendMessage(tabId, { action: 'ping' }, (response) => {
        if (!response) {
          // Content script가 없으면 주입
          chrome.scripting.executeScript({
            target: { tabId: tabId },
            files: ['content.js']
          });
        }
      });
    }
  }
});

// 아이콘 클릭 시 팝업 대신 직접 동작
chrome.action.onClicked.addListener((tab) => {
  // 팝업이 설정되어 있으면 이 이벤트는 작동하지 않음
  console.log('Extension icon clicked');
});