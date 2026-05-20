import { execSync } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';
import { VideoConfig } from '../types';

export class AdvancedFFmpegRenderer {
  static async render(config: VideoConfig, outputPath: string): Promise<void> {
    console.log('🎬 고급 FFmpeg 렌더링 시작...');
    
    const tempDir = path.join(__dirname, '../../temp', config.id);
    if (!fs.existsSync(tempDir)) {
      fs.mkdirSync(tempDir, { recursive: true });
    }
    
    try {
      const videos: string[] = [];
      const sortedImages = config.images.sort((a, b) => a.order - b.order);
      
      for (let i = 0; i < sortedImages.length; i++) {
        const img = sortedImages[i];
        const tempVideoPath = path.join(tempDir, `part_${i}.mp4`);
        videos.push(tempVideoPath);
        
        // 각 이미지에 대한 효과 구성
        const filters = this.buildFilters(config, i, sortedImages.length);
        
        const fadeCmd = [
          'ffmpeg',
          '-loop 1',
          `-i "${img.path}"`,
          `-t ${config.duration}`,
          `-vf "${filters}"`,
          '-c:v libx264',
          '-preset fast',
          '-crf 23',
          '-r 30',
          '-pix_fmt yuv420p',
          '-y',
          `"${tempVideoPath}"`
        ].join(' ');
        
        console.log(`🎬 이미지 ${i + 1}/${sortedImages.length} 처리 중...`);
        execSync(fadeCmd, { stdio: 'pipe' });
      }
      
      // 오디오 추가 여부 확인
      let finalOutput = outputPath;
      if (config.music) {
        finalOutput = path.join(tempDir, 'temp_video.mp4');
      }
      
      // 비디오 파일 리스트 생성
      const fileListPath = path.join(tempDir, 'filelist.txt');
      const fileListContent = videos.map(v => `file '${v}'`).join('\n');
      fs.writeFileSync(fileListPath, fileListContent);
      
      // 모든 파트를 하나로 합치기
      const concatCmd = [
        'ffmpeg',
        '-f concat',
        '-safe 0',
        `-i "${fileListPath}"`,
        '-c copy',
        '-y',
        `"${finalOutput}"`
      ].join(' ');
      
      console.log('🎥 비디오 합치는 중...');
      execSync(concatCmd, { stdio: 'pipe' });
      
      // 배경 음악 추가
      if (config.music) {
        console.log('🎵 배경 음악 추가 중...');
        const audioCmd = [
          'ffmpeg',
          `-i "${finalOutput}"`,
          `-i "${config.music}"`,
          '-c:v copy',
          '-c:a aac',
          '-shortest',
          '-y',
          `"${outputPath}"`
        ].join(' ');
        execSync(audioCmd, { stdio: 'pipe' });
      }
      
      console.log('✅ 렌더링 완료:', outputPath);
      
      // 임시 파일 삭제
      fs.rmSync(tempDir, { recursive: true, force: true });
      
    } catch (error) {
      if (fs.existsSync(tempDir)) {
        fs.rmSync(tempDir, { recursive: true, force: true });
      }
      throw error;
    }
  }
  
  private static buildFilters(config: any, index: number, totalImages: number): string {
    const filters: string[] = [];
    
    // 1. 기본 스케일링
    filters.push('scale=1920:1080:force_original_aspect_ratio=decrease');
    filters.push('pad=1920:1080:(ow-iw)/2:(oh-ih)/2');
    
    // 2. 전환 효과 (transition)
    const transitionDuration = 0.5;
    const fadeInEnd = transitionDuration;
    const fadeOutStart = config.duration - transitionDuration;
    
    switch (config.transition) {
      case 'fade':
        filters.push(`fade=t=in:st=0:d=${transitionDuration}`);
        filters.push(`fade=t=out:st=${fadeOutStart}:d=${transitionDuration}`);
        break;
      case 'slide':
        // 슬라이드 효과 (좌우로 이동)
        const direction = index % 2 === 0 ? 1 : -1;
        filters.push(`zoompan=z='1':x='if(lte(on,15),${direction}*1920*(on/15),0)':d=1:s=1920x1080:fps=30`);
        break;
      case 'zoom':
        // 줌 인/아웃 효과
        filters.push(`zoompan=z='if(lte(zoom,1.0),1.5,max(1.001,zoom-0.0015))':d=${config.duration * 30}:s=1920x1080:fps=30`);
        break;
      case 'rotate':
        // 회전 효과
        filters.push(`rotate=a='2*PI*t/${config.duration}':fillcolor=black@0`);
        filters.push(`fade=t=in:st=0:d=${transitionDuration}`);
        filters.push(`fade=t=out:st=${fadeOutStart}:d=${transitionDuration}`);
        break;
      case 'blur':
        // 블러 페이드 효과
        filters.push(`boxblur=luma_radius='min(10,10-10*t/${transitionDuration})':enable='between(t,0,${transitionDuration})'`);
        filters.push(`boxblur=luma_radius='min(10,10*(t-${fadeOutStart})/${transitionDuration})':enable='between(t,${fadeOutStart},${config.duration})'`);
        break;
      case 'dissolve':
        // 디졸브 효과
        filters.push(`fade=t=in:st=0:d=${transitionDuration}:alpha=1`);
        filters.push(`fade=t=out:st=${fadeOutStart}:d=${transitionDuration}:alpha=1`);
        break;
      case 'wipe':
        // 와이프 효과 (커튼처럼)
        filters.push(`crop=w='iw*min(1,t/${transitionDuration})':h=ih:x=0:y=0`);
        filters.push('pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black');
        break;
      default:
        // 기본 페이드
        filters.push(`fade=t=in:st=0:d=${transitionDuration}`);
        filters.push(`fade=t=out:st=${fadeOutStart}:d=${transitionDuration}`);
    }
    
    // 3. 색상 효과 (colorEffect)
    if (config.colorEffect) {
      switch (config.colorEffect) {
        case 'sepia':
          filters.push('colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131');
          break;
        case 'grayscale':
          filters.push('hue=s=0');
          break;
        case 'vintage':
          filters.push('curves=preset=vintage');
          filters.push('vignette');
          break;
        case 'bright':
          filters.push('eq=brightness=0.2:contrast=1.2');
          break;
        case 'dark':
          filters.push('eq=brightness=-0.2:contrast=1.1');
          break;
        case 'warm':
          filters.push('colorbalance=rs=0.3:gs=0.1:bs=-0.2');
          break;
        case 'cold':
          filters.push('colorbalance=rs=-0.2:gs=-0.1:bs=0.3');
          break;
        case 'film':
          filters.push('curves=preset=lighter');
          filters.push('noise=alls=10:allf=t+u');
          break;
      }
    }
    
    // 4. 모션 효과 (motionEffect)
    if (config.motionEffect) {
      switch (config.motionEffect) {
        case 'kenburns':
          // Ken Burns 효과 (천천히 줌인하면서 패닝)
          const zoomSpeed = 0.001;
          const panDirection = index % 2 === 0 ? 'iw-iw*zoom' : '0';
          filters.push(`zoompan=z='min(1.3,1+${zoomSpeed}*on)':x='${panDirection}':y='ih/2-(ih/zoom/2)':d=${config.duration * 30}:s=1920x1080:fps=30`);
          break;
        case 'shake':
          // 흔들림 효과
          filters.push(`crop=in_w-20:in_h-20:x='10*sin(t*10)':y='10*cos(t*10)'`);
          filters.push('pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black');
          break;
        case 'pulse':
          // 펄스 효과 (확대/축소 반복)
          filters.push(`zoompan=z='1+0.1*sin(2*PI*t/${config.duration})':d=${config.duration * 30}:s=1920x1080:fps=30`);
          break;
        case 'drift':
          // 천천히 표류하는 효과
          filters.push(`zoompan=z='1.2':x='iw/10*sin(2*PI*t/${config.duration}/2)':y='ih/10*cos(2*PI*t/${config.duration}/2)':d=${config.duration * 30}:s=1920x1080:fps=30`);
          break;
      }
    }
    
    // 5. 프레임 효과 (frameEffect)
    if (config.frameEffect) {
      switch (config.frameEffect) {
        case 'vignette':
          filters.push('vignette');
          break;
        case 'border':
          filters.push('drawbox=x=20:y=20:w=iw-40:h=ih-40:color=white:thickness=5');
          break;
        case 'rounded':
          filters.push('format=yuva444p');
          filters.push('geq=lum=\'lum(X,Y)\':a=\'if(gt(abs(W/2-X),W/2-50)*gt(abs(H/2-Y),H/2-50),if(lte(hypot(min(W/2-50-abs(W/2-X),0),min(H/2-50-abs(H/2-Y),0)),50),255,0),255)\'');
          break;
        case 'polaroid':
          filters.push('pad=iw+100:ih+140:50:50:white');
          break;
      }
    }
    
    // 6. 텍스트 오버레이 (caption) - drawtext 필터 제거 (호환성 문제)
    // drawtext는 ffmpeg가 fontconfig와 함께 컴파일되어야 작동함
    // 대신 자막을 별도로 처리하거나 이미지에 직접 오버레이하는 방식 필요
    
    // 7. 속도 효과 (speedEffect)
    if (config.speedEffect) {
      switch (config.speedEffect) {
        case 'slowmo':
          filters.push('setpts=2*PTS');
          break;
        case 'timelapse':
          filters.push('setpts=0.5*PTS');
          break;
      }
    }
    
    // 포맷 설정
    filters.push('format=yuv420p');
    
    return filters.join(',');
  }
}