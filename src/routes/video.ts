import express from 'express';
import { PrismaClient } from '@prisma/client';
import { videoQueue } from '../services/video-queue';
import path from 'path';

const router = express.Router();
const prisma = new PrismaClient();

// 모든 비디오 목록 가져오기
router.get('/', async (req, res) => {
  try {
    const videos = await prisma.video.findMany({
      orderBy: { createdAt: 'desc' },
      include: { images: true }
    });
    res.json(videos);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch videos' });
  }
});

router.post('/:videoId/render', async (req, res) => {
  try {
    const { videoId } = req.params;

    const video = await prisma.video.findUnique({
      where: { id: videoId },
      include: { images: { orderBy: { order: 'asc' } } },
    });

    if (!video) {
      return res.status(404).json({ error: 'Video not found' });
    }

    if (video.images.length === 0) {
      return res.status(400).json({ error: '이미지가 없습니다' });
    }

    const outputPath = path.join(
      __dirname,
      '../../public/output',
      `${videoId}.mp4`
    );

    await videoQueue.add('render-video', {
      videoId,
      outputPath,
    });

    res.json({
      message: '렌더링 큐에 추가되었습니다',
      videoId,
    });
  } catch (error: any) {
    console.error('Render error:', error);
    res.status(500).json({ error: error.message });
  }
});

router.get('/:videoId', async (req, res) => {
  try {
    const { videoId } = req.params;

    const video = await prisma.video.findUnique({
      where: { id: videoId },
      include: { images: { orderBy: { order: 'asc' } } },
    });

    if (!video) {
      return res.status(404).json({ error: 'Video not found' });
    }

    res.json(video);
  } catch (error: any) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/', async (req, res) => {
  try {
    const videos = await prisma.video.findMany({
      include: { images: true },
      orderBy: { createdAt: 'desc' },
    });
    res.json(videos);
  } catch (error: any) {
    res.status(500).json({ error: error.message });
  }
});

export { router as videoRouter };
