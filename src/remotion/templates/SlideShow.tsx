import React from 'react';
import { AbsoluteFill, Img, useCurrentFrame, interpolate } from 'remotion';
import { ImageData } from '../../types';

interface Props {
  image: ImageData;
  transition: string;
  fps: number;
  duration: number;
}

export const SlideShow: React.FC<Props> = ({ image, fps, duration }) => {
  const frame = useCurrentFrame();
  const durationInFrames = duration * fps;
  const transitionFrames = 15;

  const opacity = interpolate(
    frame,
    [0, transitionFrames, durationInFrames - transitionFrames, durationInFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  return (
    <AbsoluteFill style={{ opacity }}>
      <Img
        src={image.path}
        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
      />
    </AbsoluteFill>
  );
};
