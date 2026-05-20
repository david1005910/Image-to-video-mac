import { execSync } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';
import { VideoConfig } from '../types';

export class FFmpegRenderer {
  static async render(config: VideoConfig, outputPath: string): Promise<void> {
    console.log('🎬 FFmpeg 렌더링 시작...');
    
    // 임시 디렉토리 생성
    const tempDir = path.join(__dirname, '../../temp', config.id);
    if (!fs.existsSync(tempDir)) {
      fs.mkdirSync(tempDir, { recursive: true });
    }
    
    try {
      // 이미지별 비디오 생성
      const videos: string[] = [];
      
      for (let i = 0; i < config.images.length; i++) {
        const img = config.images.sort((a, b) => a.order - b.order)[i];
        const tempVideoPath = path.join(tempDir, `part_${i}.mp4`);
        videos.push(tempVideoPath);
        
        // 각 이미지를 비디오로 변환 (페이드 효과 포함)
        const fadeCmd = [
          'ffmpeg',
          '-loop 1',
          `-i "${img.path}"`,
          `-t ${config.duration}`,
          '-vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,',
          `fade=t=in:st=0:d=0.5,fade=t=out:st=${config.duration - 0.5}:d=0.5,format=yuv420p"`,
          '-c:v libx264',
          '-preset fast',
          '-crf 23',
          '-r 30',
          '-pix_fmt yuv420p',
          '-y',
          `"${tempVideoPath}"`
        ].join(' ');
        
        console.log(`🎬 이미지 ${i + 1}/${config.images.length} 처리 중...`);
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
      // 임시 파일 삭제
      if (fs.existsSync(tempDir)) {
        fs.rmSync(tempDir, { recursive: true, force: true });
      }
      throw error;
    }
  }
}