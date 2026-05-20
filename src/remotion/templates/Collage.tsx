import React from 'react';
import { AbsoluteFill, Img, useCurrentFrame, interpolate } from 'remotion';
import { ImageData } from '../../types';

interface Props {
  image: ImageData;
  transition: string;
  fps: number;
  duration: number;
}

export const Collage: React.FC<Props> = ({ image, fps, duration }) => {
  const frame = useCurrentFrame();
  const durationInFrames = duration * fps;

  const slideX = interpolate(
    frame,
    [0, 20],
    [image.order % 2 === 0 ? 1920 : -1920, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  const opacity = interpolate(
    frame,
    [0, 10, durationInFrames - 10, durationInFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  return (
    <AbsoluteFill style={{ opacity }}>
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          transform: `translateX(${slideX}px)`,
        }}
      >
        <Img
          src={image.path}
          style={{
            maxWidth: '90%',
            maxHeight: '90%',
            objectFit: 'contain',
            boxShadow: '0 20px 60px rgba(0,0,0,0.5)',
          }}
        />
      </div>
    </AbsoluteFill>
  );
};
