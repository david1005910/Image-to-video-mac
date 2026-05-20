export interface VideoConfig {
  id: string;
  title: string;
  style: 'slideshow' | 'kenburns' | 'collage';
  duration: number;
  transition: 'fade' | 'slide' | 'zoom' | 'rotate' | 'blur' | 'dissolve' | 'wipe' | 'none';
  colorEffect?: 'sepia' | 'grayscale' | 'vintage' | 'bright' | 'dark' | 'warm' | 'cold' | 'film' | null;
  motionEffect?: 'kenburns' | 'shake' | 'pulse' | 'drift' | null;
  frameEffect?: 'vignette' | 'border' | 'rounded' | 'polaroid' | null;
  textPosition?: 'bottom' | 'top' | 'center' | 'bottom-left' | 'bottom-right';
  captions?: string[];
  speedEffect?: 'slowmo' | 'timelapse' | null;
  music?: string;
  fps: number;
  width: number;
  height: number;
  images: ImageData[];
}

export interface ImageData {
  id: string;
  path: string;
  order: number;
  width: number;
  height: number;
  caption?: string;
}

export interface RenderJob {
  videoId: string;
  outputPath: string;
}
