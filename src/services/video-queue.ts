import { Queue } from 'bullmq';
import { RenderJob } from '../types';

const connection = {
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379'),
};

export const videoQueue = new Queue<RenderJob>('video-rendering', {
  connection,
});
