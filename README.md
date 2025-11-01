# AI Analyst Platform 

> An AI-powered startup analysis platform that automates investment due diligence by analyzing pitch decks, videos, and competitor intelligence.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini_2.5_Flash-4285F4.svg)](https://ai.google.dev)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB.svg)](https://www.python.org)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Frontend Interface](#-frontend-interface)
- [Deployment](#-deployment)
- [Contributing](#-contributing)

---

## ✨ Features

### 🎥 **Video Pitch Analyzer**
- Analyze YouTube video pitches via URL
- Upload and process video files (MP4, MOV, AVI)
- Extract key insights, executive summaries, and timestamped moments
- Audio transcription using Faster-Whisper

### 📄 **Document Intelligence**
- Extract tables and charts from PDF pitch decks
- OCR and structured data extraction using Gemini Vision
- Page-by-page analysis with visual previews
- Interactive chart rendering with Chart.js

### 💬 **RAG-Powered Chat**
- Upload documents for interactive Q&A
- Vector-based semantic search with ChromaDB
- Context-aware responses powered by Gemini
- Real-time conversational analysis

### 🔍 **Competitor Analysis**
- Live website scraping with Crawl4AI
- Automated competitive intelligence extraction
- Business model, pricing, and feature comparison
- Market positioning analysis

### 📊 **Interactive Dashboard**
- Real-time data visualization
- Multi-stage loading indicators
- Exportable reports (JSON and TXT formats)
- Responsive design with light/dark mode

---

## 🛠 Tech Stack

### **Backend**
- **Framework**: FastAPI 0.115.0
- **AI/ML**: Google Gemini 2.5 Flash API
- **Vector Store**: ChromaDB 0.5.23
- **Web Scraping**: Crawl4AI 0.4.24
- **PDF Processing**: PyMuPDF (fitz) 1.24.14
- **Video Processing**: FFmpeg, Faster-Whisper 1.1.0
- **Text Processing**: LangChain Text Splitters

### **Frontend**
- **Pure HTML5, CSS3, Vanilla JavaScript**
- **Charting**: Chart.js 4.4.0
- **Markdown**: Marked.js 11.0.0

### **Infrastructure**
- **Python**: 3.8+
- **Database**: ChromaDB (vector storage)
- **Cloud**: Google Cloud Platform ready

---

## 📁 Project Structure

```
ai-analyst-platform/
├── backend/                      # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration settings
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes/
│   │   │       ├── __init__.py
│   │   │       ├── video_pitch.py
│   │   │       ├── rag.py
│   │   │       └── competitor.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── video_service.py
│   │   │   ├── rag_service.py
│   │   │   ├── competitor_service.py
│   │   │   └── gemini_service.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── request_models.py
│   │   │   └── response_models.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   └── logger.py
│   │   └── core/
│   │       ├── __init__.py
│   │       └── clients.py
│   ├── uploads/                 # Temporary file storage
│   ├── chroma_db/               # ChromaDB vector store
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/                     # Frontend Application
│   └── index.html               # Single-page application
│
├── .gitignore
└── README.md                     # This file
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- FFmpeg (for video processing)
- Google Gemini API key

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/ai-analyst-platform.git
cd ai-analyst-platform
```

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Install FFmpeg (Optional - for video upload feature)

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

---

## ⚙️ Configuration

### Create Environment File

```bash
cd backend
cp .env.example .env
```

### Edit `.env` File

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional (defaults provided)
API_TITLE=AI Analyst Platform API
API_VERSION=1.0.0
MAX_UPLOAD_SIZE=52428800
MAX_PAGES_PDF=10
MAX_PAGES_RAG=5
CHUNK_SIZE=1500
CHUNK_OVERLAP=300
WHISPER_MODEL=base
WHISPER_DEVICE=cpu
WHISPER_COMPUTE_TYPE=int8
```

### Get Your Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Copy and paste it into your `.env` file

---

## 🎮 Running the Application

### Start the Backend Server

```bash
cd backend

# Option 1: Direct run
python -m app.main

# Option 2: With hot reload (development)
uvicorn app.main:app --reload

# Option 3: Custom host/port
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The backend will be available at: **http://localhost:8000**

### Open the Frontend

```bash
cd frontend

# Option 1: Using Python's built-in server
python -m http.server 3000

# Option 2: Using Node.js http-server (if installed)
npx http-server -p 3000

# Option 3: Open directly in browser
# Simply open index.html in your browser
```

The frontend will be available at: **http://localhost:3000**

### Access the Application

1. **Frontend UI**: http://localhost:3000
2. **Backend API**: http://localhost:8000
3. **API Docs (Swagger)**: http://localhost:8000/docs
4. **API Docs (ReDoc)**: http://localhost:8000/redoc

---

## 📖 API Documentation

### Video Pitch Endpoints

#### Analyze YouTube Video
```http
POST /api/video-pitch/analyze
Content-Type: application/json

{
  "youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

#### Upload Video File
```http
POST /api/video-pitch/upload
Content-Type: multipart/form-data

file: [video file]
```

### RAG Analyzer Endpoints

#### Upload Document
```http
POST /api/rag/upload
Content-Type: multipart/form-data

file: [PDF file]
```

#### Query Documents
```http
POST /api/rag/query
Content-Type: application/json

{
  "query": "What is the company's revenue model?",
  "collection_name": "user_documents"
}
```

### Competitor Analysis Endpoint

#### Analyze Competitor
```http
POST /api/competitor/analyze
Content-Type: application/json

{
  "company_name": "TechStartup Inc.",
  "company_url": "https://www.techstartup.com"
}
```

---

## 🎨 Frontend Interface

### Features

- **Dashboard**: Central hub with quick action cards
- **AI Analyzer**: PDF document analysis and data extraction
- **RAG Analyzer**: Document upload and interactive Q&A
- **Competitor Analyzer**: Live website competitive intelligence
- **Video Pitch Analyzer**: YouTube and video file analysis
- **Light/Dark Mode**: Automatic theme switching
- **Export Capabilities**: JSON and TXT report generation

### Design System

- Custom CSS variables with Perplexity-inspired design tokens
- Responsive layouts with mobile-first approach
- Accessible components with ARIA labels
- Smooth animations and transitions

---

## 🚢 Deployment

### Backend Deployment (Google Cloud Run)

```bash
# Build Docker image
docker build -t ai-analyst-backend ./backend

# Tag for Google Container Registry
docker tag ai-analyst-backend gcr.io/YOUR_PROJECT_ID/ai-analyst-backend

# Push to registry
docker push gcr.io/YOUR_PROJECT_ID/ai-analyst-backend

# Deploy to Cloud Run
gcloud run deploy ai-analyst-backend \
  --image gcr.io/YOUR_PROJECT_ID/ai-analyst-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Frontend Deployment

**Option 1: Netlify / Vercel**
- Drag and drop the `frontend` folder
- No build step required (static HTML)

**Option 2: GitHub Pages**
```bash
# Push to gh-pages branch
git subtree push --prefix frontend origin gh-pages
```

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/
```

### Frontend Testing

Open `index.html` in multiple browsers:
- Chrome
- Firefox
- Safari
- Edge

---

## 📊 Performance

- **Document Processing**: < 5 minutes for 45-page reports
- **Video Transcription**: Real-time processing
- **RAG Response**: < 3 seconds
- **Competitor Analysis**: 8-12 seconds (4-stage pipeline)

---

## 🔒 Security

- Server-side file validation
- API key management via environment variables
- CORS configuration
- No client-side data persistence for sensitive data
- Secure file upload with size limits

---

## 🐛 Troubleshooting

### Common Issues

**1. ModuleNotFoundError: No module named 'app'**
```bash
# Make sure you're in the backend directory
cd backend
python -m app.main
```

**2. GEMINI_API_KEY not found**
```bash
# Check your .env file exists and contains the key
cat .env
```

**3. FFmpeg not found (video upload fails)**
```bash
# Install FFmpeg
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
```

**4. CORS errors in browser**
- Make sure backend is running on port 8000
- Frontend should access `http://localhost:8000` (not IP address)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

**Manan Jain**
- GitHub: [manan-dude](https://github.com/manan-dude)
- LinkedIn: [Manan Jain](https://www.linkedin.com/in/manan-jain-dude/)

---

## 🙏 Acknowledgments

- Google Gemini API for powerful AI capabilities
- FastAPI for the excellent web framework
- ChromaDB for vector storage
- Chart.js for data visualization

---


## 🗺️ Roadmap

- [ ] Add authentication and user management
- [ ] Implement real-time collaboration features
- [ ] Add more data source integrations
- [ ] Enhanced analytics and reporting
- [ ] Mobile application (React Native)
- [ ] Multi-language support

---

**Built with ❤️ for the Google Cloud Gen AI Exchange Hackathon 2025**
