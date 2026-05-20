import { Worker } from 'bullmq';
import { PrismaClient } from '@prisma/client';
// import { RemotionRenderer } from './renderer/remotion-renderer';
// import { FFmpegRenderer } from './renderer/ffmpeg-renderer';
// import { AdvancedFFmpegRenderer } from './renderer/advanced-ffmpeg-renderer';
import { StableFFmpegRenderer } from './renderer/stable-ffmpeg-renderer';
import { RenderJob, VideoConfig, ImageData } from './types';
import path from 'path';

const prisma = new PrismaClient();

const connection = {
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379'),
};

const worker = new Worker<RenderJob>(
  'video-rendering',
  async (job) => {
    const { videoId, outputPath } = job.data;

    try {
      console.log(`\n🎬 비디오 처리 시작: ${videoId}`);

      await prisma.video.update({
        where: { id: videoId },
        data: { status: 'processing' },
      });

      const video = await prisma.video.findUnique({
        where: { id: videoId },
        include: { images: { orderBy: { order: 'asc' } } },
      });

      if (!video) {
        throw new Error('Video not found');
      }

      const config: VideoConfig = {
        id: video.id,
        title: video.title,
        style: video.style as any,
        duration: video.duration,
        transition: video.transition as any,
        colorEffect: video.colorEffect as any,
        motionEffect: video.motionEffect as any,
        frameEffect: video.frameEffect as any,
        textPosition: video.textPosition as any,
        captions: video.captions ? video.captions.split(',').map(c => c.trim()) : undefined,
        music: video.music || undefined,
        fps: 30,
        width: 1920,
        height: 1080,
        images: video.images.map((img): ImageData => ({
          id: img.id,
          path: path.join(__dirname, '../public', img.path),
          order: img.order,
          width: img.width,
          height: img.height,
          caption: img.caption || undefined,
        })),
      };

      await StableFFmpegRenderer.render(config, outputPath);

      await prisma.video.update({
        where: { id: videoId },
        data: {
          status: 'completed',
          outputPath,
        },
      });

      console.log('✅ 비디오 완료:', videoId);
    } catch (error) {
      console.error('❌ 오류:', error);

      await prisma.video.update({
        where: { id: videoId },
        data: { status: 'failed' },
      });

      throw error;
    }
  },
  { connection, concurrency: 1 }
);

worker.on('completed', (job) => {
  console.log(`✅ Job ${job.id} 완료`);
});

worker.on('failed', (job, err) => {
  console.error(`❌ Job ${job?.id} 실패:`, err);
});

console.log('👷 Worker 시작됨');
