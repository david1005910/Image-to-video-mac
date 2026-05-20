import { bundle } from '@remotion/bundler';
import { renderMedia } from '@remotion/renderer';
import * as path from 'path';
import { VideoConfig } from '../types';

export class RemotionRenderer {
  static async render(config: VideoConfig, outputPath: string): Promise<void> {
    console.log('🎬 Remotion 렌더링 시작...');

    const bundleLocation = await bundle({
      entryPoint: path.join(__dirname, '../remotion/Root.tsx'),
      webpackOverride: (cfg) => cfg,
    });

    const totalFrames = config.images.length * config.duration * config.fps;

    await renderMedia({
      composition: 'ImageVideo' as any,
      serveUrl: bundleLocation,
      codec: 'h264',
      outputLocation: outputPath,
      inputProps: { config },
      chromiumOptions: {
        disableWebSecurity: true,
        gl: 'swiftshader',
      },
      timeoutInMilliseconds: 120000,
      onProgress: ({ renderedFrames, totalFrames }) => {
        const progress = ((renderedFrames / totalFrames) * 100).toFixed(1);
        console.log(`⏳ 진행: ${progress}% (${renderedFrames}/${totalFrames})`);
      },
    });

    console.log('✅ 렌더링 완료:', outputPath);
  }
}
