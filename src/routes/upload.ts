import express from 'express';
import multer from 'multer';
import path from 'path';
import sharp from 'sharp';
import { v4 as uuidv4 } from 'uuid';
import { PrismaClient } from '@prisma/client';

const router = express.Router();
const prisma = new PrismaClient();

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, path.join(__dirname, '../../public/uploads/'));
  },
  filename: (req, file, cb) => {
    const uniqueName = `${uuidv4()}${path.extname(file.originalname)}`;
    cb(null, uniqueName);
  },
});

const upload = multer({
  storage,
  limits: { fileSize: 50 * 1024 * 1024 },
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];
    if (allowedTypes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error('JPG, PNG, WebP, GIF만 가능합니다.'));
    }
  },
});

router.post('/', upload.array('images', 50), async (req, res) => {
  try {
    const files = req.files as Express.Multer.File[];
    
    if (!files || files.length === 0) {
      return res.status(400).json({ error: '이미지를 업로드해주세요' });
    }

    const videoId = uuidv4();
    const title = req.body.title || `Video ${new Date().toISOString()}`;

    const video = await prisma.video.create({
      data: {
        id: videoId,
        title,
        style: req.body.style || 'slideshow',
        duration: parseFloat(req.body.duration) || 3,
        transition: req.body.transition || 'fade',
        colorEffect: req.body.colorEffect || null,
        motionEffect: req.body.motionEffect || null,
        frameEffect: req.body.frameEffect || null,
        textPosition: req.body.textPosition || 'bottom',
        captions: req.body.captions || null,
        music: req.body.music || null,
      },
    });

    const imageRecords = await Promise.all(
      files.map(async (file, index) => {
        const metadata = await sharp(file.path).metadata();

        const optimizedFilename = `opt_${file.filename}`;
        const optimizedPath = path.join(
          path.dirname(file.path),
          optimizedFilename
        );

        await sharp(file.path)
          .resize(1920, 1080, {
            fit: 'cover',
            position: 'center',
          })
          .jpeg({ quality: 90 })
          .toFile(optimizedPath);

        return prisma.image.create({
          data: {
            videoId,
            filename: optimizedFilename,
            originalName: file.originalname,
            path: `/uploads/${optimizedFilename}`,
            order: index,
            width: metadata.width || 1920,
            height: metadata.height || 1080,
            size: file.size,
            mimeType: file.mimetype,
          },
        });
      })
    );

    res.json({
      message: '업로드 성공',
      videoId,
      imageCount: imageRecords.length,
    });
  } catch (error: any) {
    console.error('Upload error:', error);
    res.status(500).json({ error: error.message });
  }
});

export { router as uploadRouter };
