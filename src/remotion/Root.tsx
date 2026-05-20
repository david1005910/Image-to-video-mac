import React from 'react';
import { Composition, registerRoot } from 'remotion';
import { Video } from './Video';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="ImageVideo"
        component={Video}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{ config: null as any }}
      />
    </>
  );
};

registerRoot(RemotionRoot);
