import { execSync } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';
import { VideoConfig } from '../types';

export class StableFFmpegRenderer {
  static async render(config: VideoConfig, outputPath: string): Promise<void> {
    console.log('🎬 안정화된 FFmpeg 렌더링 시작...');
    
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
        
        // 각 이미지에 대한 효과 구성 (안정적인 필터만 사용)
        const filters = this.buildStableFilters(config, i, sortedImages.length);
        
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
        `"${outputPath}"`
      ].join(' ');
      
      console.log('🎥 비디오 합치는 중...');
      execSync(concatCmd, { stdio: 'pipe' });
      
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
  
  private static buildStableFilters(config: any, index: number, totalImages: number): string {
    const filters: string[] = [];
    
    // 1. 기본 스케일링
    filters.push('scale=1920:1080:force_original_aspect_ratio=decrease');
    filters.push('pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black');
    
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
        // 슬라이드 효과 - zoompan으로 구현
        const slideDirection = index % 2 === 0 ? '0' : 'iw-ow';
        filters.push(`zoompan=z='1':x='${slideDirection}*(1-on/15)':y='0':d=${config.duration * 30}:s=1920x1080:fps=30`);
        break;
      case 'zoom':
        // 줌 효과
        filters.push(`zoompan=z='min(2,1+on/50)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=${config.duration * 30}:s=1920x1080:fps=30`);
        break;
      case 'rotate':
        // 회전 효과
        filters.push(`rotate=a='PI*t/${config.duration}':fillcolor=black@0:ow=1920:oh=1080`);
        break;
      case 'blur':
        // 블러 효과
        const maxBlur = 10;
        filters.push(`boxblur=luma_radius='if(lt(t,${transitionDuration}),${maxBlur}*(1-t/${transitionDuration}),if(gt(t,${fadeOutStart}),${maxBlur}*(t-${fadeOutStart})/${transitionDuration},0))':chroma_radius='if(lt(t,${transitionDuration}),${maxBlur}*(1-t/${transitionDuration}),if(gt(t,${fadeOutStart}),${maxBlur}*(t-${fadeOutStart})/${transitionDuration},0))':enable='lt(t,${transitionDuration})+gt(t,${fadeOutStart})'`);
        break;
      case 'dissolve':
      case 'wipe':
        // 디졸브와 와이프는 기본 페이드로 대체
        filters.push(`fade=t=in:st=0:d=${transitionDuration}`);
        filters.push(`fade=t=out:st=${fadeOutStart}:d=${transitionDuration}`);
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
          break;
        case 'bright':
          filters.push('eq=brightness=0.2:contrast=1.2');
          break;
        case 'dark':
          filters.push('eq=brightness=-0.2:contrast=1.1');
          break;
        case 'warm':
          filters.push('eq=gamma_r=1.2:gamma_b=0.8');
          break;
        case 'cold':
          filters.push('eq=gamma_r=0.8:gamma_b=1.2');
          break;
        case 'film':
          filters.push('curves=preset=lighter');
          break;
      }
    }
    
    // 4. 모션 효과 (motionEffect) - zoompan 사용
    if (config.motionEffect && config.transition !== 'zoom' && config.transition !== 'slide') {
      switch (config.motionEffect) {
        case 'kenburns':
          // Ken Burns 효과
          const zoom = index % 2 === 0 ? '1+0.002*on' : '1.3-0.002*on';
          const xPan = index % 2 === 0 ? '0' : 'iw-ow';
          filters.push(`zoompan=z='${zoom}':x='${xPan}':y='ih/2-oh/2':d=${config.duration * 30}:s=1920x1080:fps=30`);
          break;
        case 'shake':
          // 흔들림 효과 - 작은 움직임
          filters.push(`crop=in_w-20:in_h-20:x='10+5*sin(t*10)':y='10+5*cos(t*10)'`);
          filters.push('pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black');
          break;
        case 'pulse':
        case 'drift':
          // 펄스와 드리프트는 기본 켄번즈로 대체
          filters.push(`zoompan=z='1.1+0.05*sin(2*PI*t/${config.duration})':x='iw/2-ow/2':y='ih/2-oh/2':d=${config.duration * 30}:s=1920x1080:fps=30`);
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
          filters.push('drawbox=x=10:y=10:w=iw-20:h=ih-20:color=white:thickness=5');
          break;
        case 'rounded':
          // 둥근 모서리는 복잡하므로 비네트로 대체
          filters.push('vignette=angle=PI/4');
          break;
        case 'polaroid':
          // 폴라로이드 프레임
          filters.push('pad=iw+100:ih+140:50:50:white');
          break;
      }
    }
    
    // 포맷 설정
    filters.push('format=yuv420p');
    
    return filters.join(',');
  }
}