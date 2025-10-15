# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

This is a full-stack web application for intelligent avatar replacement in chat screenshots. The project consists of:

- **Frontend**: Vue 3 + Element Plus SPA with Canvas-based template selection
- **Backend**: FastAPI service with OpenCV-based image processing
- **Core Algorithm**: Template matching for avatar detection and replacement

### Key Components

**Frontend Architecture:**
- `src/stores/app.js` - Pinia store managing session state, progress, and processing results
- `src/components/ImageUpload.vue` - Drag-and-drop image upload with preview
- `src/components/TemplateSelector.vue` - Canvas-based ROI selection using Konva.js
- `src/views/AvatarReplace.vue` - Main workflow orchestration

**Backend Architecture:**
- `app/session_manager.py` - UUID-based session management with automatic cleanup
- `modules/web_adapter.py` - Main processing orchestrator that coordinates detection and replacement
- `modules/avatar_detector.py` - Template matching algorithm for avatar detection
- `modules/avatar_replacer.py` - Image processing for avatar replacement
- `app/routers/` - FastAPI route handlers for session and file upload endpoints

### Processing Pipeline

1. **Session Creation**: Frontend creates session via `/api/session/create`
2. **File Upload**: Chat screenshot and new avatar uploaded to session temp directory
3. **Template Selection**: User selects avatar region on Canvas, coordinates sent as bbox
4. **Detection**: `WebChatAvatarReplacer` uses template matching to find similar avatars
5. **Replacement**: Detected avatars replaced with new avatar, maintaining aspect ratios
6. **Result**: Processed image returned with detection metadata

## Development Commands

### Frontend (Vue.js)
```bash
cd frontend
npm install                 # Install dependencies
npm run dev                # Start development server (localhost:3000)
npm run build              # Build for production
npm run preview            # Preview production build
```

### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt    # Install Python dependencies
python main.py                     # Start development server (localhost:8000)
# OR
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation
- Swagger UI: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### Production Deployment (Render)
The project includes `render.yaml` for automated deployment:
- Frontend: Static site built from `frontend/dist`
- Backend: Python web service with auto-deploy

## API Integration

The frontend uses Axios with a proxy configuration for API calls:
- Development: Frontend proxies `/api/*` to `http://localhost:8000`
- API base URL configured in `src/api/request.js`
- Session management in `src/api/session.js`
- File operations in `src/api/upload.js`

## State Management

The app uses Pinia with a single store (`useAppStore`) that manages:
- Session lifecycle and progress tracking
- Uploaded image files and template coordinates
- Detection results and processed output
- Real-time progress updates from backend

## Image Processing Details

- **Template Detection**: OpenCV template matching with configurable threshold
- **Right-side Filtering**: Filters chat bubbles based on screen position
- **Avatar Replacement**: Maintains aspect ratio and applies edge blending
- **File Formats**: Supports common image formats (PNG, JPG, WebP)

## Session Management

- UUID-based sessions with temporary file storage
- Automatic cleanup of expired sessions (configurable timeout)
- Progress tracking with real-time updates to frontend
- Stateful processing pipeline with checkpoint recovery