// Node.js 스크립트로 아이콘 생성
const fs = require('fs');

// SVG 아이콘 생성
const createSVGIcon = (size) => {
    const center = size / 2;
    const scale = size / 128;
    
    return `<?xml version="1.0" encoding="UTF-8"?>
<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">
    <!-- 배경 원 (그라디언트) -->
    <defs>
        <radialGradient id="bg-gradient-${size}">
            <stop offset="0%" style="stop-color:#764ba2;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#667eea;stop-opacity:1" />
        </radialGradient>
    </defs>
    
    <!-- 배경 -->
    <circle cx="${center}" cy="${center}" r="${center * 0.9}" fill="url(#bg-gradient-${size})" />
    
    <!-- 비디오 카메라 아이콘 -->
    <!-- 카메라 본체 -->
    <rect x="${center - 30 * scale}" y="${center - 20 * scale}" 
          width="${60 * scale}" height="${40 * scale}" 
          fill="white" rx="${5 * scale}" />
    
    <!-- 카메라 렌즈 -->
    <circle cx="${center + 15 * scale}" cy="${center}" r="${15 * scale}" fill="#333" />
    <circle cx="${center + 15 * scale}" cy="${center}" r="${5 * scale}" fill="#666" />
    
    <!-- 녹화 표시 -->
    <circle cx="${center - 20 * scale}" cy="${center - 10 * scale}" r="${5 * scale}" fill="#ff0000">
        <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
    </circle>
    
    <!-- 플레이 버튼 -->
    <path d="M ${center - 10 * scale} ${center - 12 * scale} 
             L ${center - 10 * scale} ${center + 12 * scale} 
             L ${center + 8 * scale} ${center} Z" 
          fill="rgba(255,255,255,0.8)" />
</svg>`;
};

// 각 크기별 SVG 생성
const sizes = [128, 48, 16];

sizes.forEach(size => {
    const svg = createSVGIcon(size);
    const filename = `icon-${size}.svg`;
    fs.writeFileSync(filename, svg);
    console.log(`Created ${filename}`);
});

console.log('\n✅ SVG 아이콘 생성 완료!');
console.log('SVG를 PNG로 변환하려면 온라인 변환기를 사용하거나 브라우저에서 열어 저장하세요.');