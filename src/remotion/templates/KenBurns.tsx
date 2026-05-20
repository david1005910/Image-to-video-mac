import React from 'react';
import { AbsoluteFill, Img, useCurrentFrame, interpolate } from 'remotion';
import { ImageData } from '../../types';

interface Props {
  image: ImageData;
  transition: string;
  fps: number;
  duration: number;
}

export const KenBurns: React.FC<Props> = ({ image, fps, duration }) => {
  const frame = useCurrentFrame();
  const durationInFrames = duration * fps;

  const scale = interpolate(frame, [0, durationInFrames], [1, 1.2], {
    extrapolateRight: 'clamp',
  });

  const panX = interpolate(
    frame,
    [0, durationInFrames],
    [0, (image.order % 2 === 0 ? 1 : -1) * 50],
    { extrapolateRight: 'clamp' }
  );

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
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          transform: `scale(${scale}) translateX(${panX}px)`,
        }}
      />
    </AbsoluteFill>
  );
};
