# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development
- `npm run setup` - Initial project setup (installs deps, sets up database, creates directories)
- `npm start` - Starts both server and worker concurrently
- `npm run dev` - Development server only (port 3000)
- `npm run worker` - Video processing worker only
- `npm run preview` - Preview Remotion compositions

### Database
- `npm run db:setup` - Initialize Prisma and run migrations
- `npx prisma studio` - Visual database editor
- `npx prisma migrate dev` - Create new migration

## Architecture

This is a Remotion-based video generation app that converts images to videos:

### Core Components
1. **Express Server** (`src/server.ts`): HTTP API and web interface
2. **BullMQ Worker** (`src/worker.ts`): Background video rendering queue processor
3. **Remotion Renderer** (`src/renderer/remotion-renderer.ts`): Video generation using Remotion
4. **SQLite + Prisma**: Data persistence for videos and images
5. **Redis + BullMQ**: Job queue for async video processing

### Video Templates (`src/remotion/templates/`)
- **SlideShow.tsx**: Fade transitions between images
- **KenBurns.tsx**: Documentary-style zoom/pan effects  
- **Collage.tsx**: Slide-in animations

### Processing Flow
1. User uploads images via web UI → stored in `public/uploads/`
2. Server creates database records and queues render job
3. Worker picks up job, invokes Remotion renderer
4. Rendered video saved to `public/output/`
5. User downloads completed video

### Dependencies
- Redis must be running (`brew services start redis`)
- Environment variables in `.env` file
- TypeScript with ts-node for development