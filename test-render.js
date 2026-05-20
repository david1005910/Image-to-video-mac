const { bundle } = require('@remotion/bundler');
const { renderMedia } = require('@remotion/renderer');
const path = require('path');

async function testRender() {
  try {
    console.log('Starting test render...');
    
    const bundleLocation = await bundle({
      entryPoint: path.join(__dirname, 'src/remotion/Root.tsx'),
      webpackOverride: (cfg) => cfg,
    });
    
    console.log('Bundle created:', bundleLocation);
    
    const testConfig = {
      id: 'test',
      title: 'Test Video',
      style: 'slideshow',
      duration: 2,
      transition: 'fade',
      fps: 30,
      width: 1920,
      height: 1080,
      images: [
        {
          id: '1',
          path: path.join(__dirname, 'public/uploads/24d29458-79bb-4803-af09-30e4a700766b.jpg'),
          order: 0,
          width: 1920,
          height: 1080
        },
        {
          id: '2',
          path: path.join(__dirname, 'public/uploads/2d7d1612-00f4-4dde-98ca-3744122cbd75.jpg'),
          order: 1,
          width: 1920,
          height: 1080
        }
      ]
    };
    
    console.log('Starting render with config:', testConfig);
    
    await renderMedia({
      composition: 'ImageVideo',
      serveUrl: bundleLocation,
      codec: 'h264',
      outputLocation: path.join(__dirname, 'public/output/test.mp4'),
      inputProps: { config: testConfig },
      onProgress: ({ renderedFrames, totalFrames }) => {
        const progress = ((renderedFrames / totalFrames) * 100).toFixed(1);
        console.log(`Progress: ${progress}% (${renderedFrames}/${totalFrames})`);
      },
    });
    
    console.log('Render completed!');
  } catch (error) {
    console.error('Error:', error);
  }
}

testRender();