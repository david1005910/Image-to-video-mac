import React from 'react';
import { AbsoluteFill, Sequence, Audio } from 'remotion';
import { VideoConfig } from '../types';
import { SlideShow } from './templates/SlideShow';
import { KenBurns } from './templates/KenBurns';
import { Collage } from './templates/Collage';

export const Video: React.FC<{ config: VideoConfig }> = ({ config }) => {
  const fps = config.fps;
  const durationPerImage = Math.round(config.duration * fps);

  const Template =
    config.style === 'kenburns'
      ? KenBurns
      : config.style === 'collage'
      ? Collage
      : SlideShow;

  return (
    <AbsoluteFill style={{ backgroundColor: 'black' }}>
      {config.images.map((image, index) => {
        const from = index * durationPerImage;
        return (
          <Sequence key={image.id} from={from} durationInFrames={durationPerImage}>
            <Template
              image={image}
              transition={config.transition}
              fps={fps}
              duration={config.duration}
            />
          </Sequence>
        );
      })}
      {config.music && <Audio src={config.music} />}
    </AbsoluteFill>
  );
};
