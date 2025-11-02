# AI Analyst - Frontend

> A comprehensive AI-powered platform for startup intelligence and analysis. Built for the Google AI Hackathon.

![AI Analyst](https://img.shields.io/badge/AI-Analyst-teal?style=for-the-badge)
![React](https://img.shields.io/badge/React-18-blue?style=for-the-badge&logo=react)
![Vite](https://img.shields.io/badge/Vite-5-purple?style=for-the-badge&logo=vite)
![TailwindCSS](https://img.shields.io/badge/Tailwind-3-38bdf8?style=for-the-badge&logo=tailwindcss)

## 🎯 Overview

**AI Analyst** is an all-in-one strategic intelligence platform that centralizes and accelerates startup analysis. From competitor research to document Q&A, this platform leverages Google's AI tools to provide actionable insights in seconds.

### Key Features

- 📊 **Competitor Analysis** - Deep competitor intelligence with structured reports
- 🎥 **Video Pitch Analyzer** - Extract insights from YouTube pitch videos
- 📄 **AI Analyzer** - Extract tables, plots, and generate summaries from PDFs
- 💬 **Ask Your Startup** - RAG-powered document Q&A system
- 🌙 **Dark Mode** - Beautiful, responsive UI with dark mode support
- 📱 **Mobile-First** - Fully responsive across all devices

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend API running (see backend README)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd ai-analyst-frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Configure your environment variables
# Edit .env and add your backend URL
VITE_API_BASE_URL=http://localhost:8000

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

## 📦 Tech Stack

### Core

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **TanStack Query** - Data fetching and caching

### UI & Styling

- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Animation library
- **Lucide React** - Icon library
- **React Hot Toast** - Toast notifications

### Additional Libraries

- **React Markdown** - Markdown rendering (for chat)
- **Remark GFM** - GitHub Flavored Markdown support

## 📁 Project Structure

```
src/
├── components/
│   ├── features/          # Main feature components
│   │   ├── Dashboard.jsx
│   │   ├── CompetitorAnalysis.jsx
│   │   ├── VideoPitchAnalyzer.jsx
│   │   ├── AIAnalyzer.jsx
│   │   └── AskYourStartup.jsx
│   ├── layout/            # Layout components
│   │   ├── Layout.jsx
│   │   ├── Sidebar.jsx
│   │   └── Header.jsx
│   └── ui/                # Reusable UI components
│       ├── Button.jsx
│       ├── Card.jsx
│       └── Input.jsx
├── context/               # React Context providers
│   └── ActivityContext.jsx
├── services/              # API services
│   └── api.js
├── App.jsx               # Main app component
├── main.jsx              # Entry point
└── index.css             # Global styles
```

## 🎨 Features Overview

### 1. Dashboard
- Overview of all modules
- Recent activity tracking
- Quick navigation to all features

### 2. Competitor Analysis
- Enter competitor URL and company name
- AI-powered analysis of:
  - Market position
  - Target audience
  - Pricing strategy
  - Technology stack
  - Strengths and weaknesses
  - Recent news
- Export results as JSON

### 3. Video Pitch Analyzer
- Paste YouTube video URL
- Extract:
  - Video summary
  - Key talking points
  - Potential investor questions
- Save and export analysis

### 4. AI Analyzer
- Drag & drop PDF upload
- Two-tab interface:
  - **Document Summary**: AI-generated insights, financial metrics, recommendations
  - **Extracted Visualizations**: Tables (rendered as HTML), plots, page screenshots
- Edge case handling with fallbacks
- Export full analysis

### 5. Ask Your Startup
- Upload PDF documents
- RAG-powered Q&A system
- Chat interface with markdown support
- Real-time responses
- Document chunking and indexing

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Backend API URL
VITE_API_BASE_URL=http://localhost:8000

# Optional: Enable debug mode
VITE_DEBUG=false
```

### API Integration

All API calls go through the centralized service layer in `src/services/api.js`:

```javascript
// Example API structure
export const competitorAPI = {
  analyze: (name, url) => fetch(`${BASE_URL}/api/competitor/analyze`, {...})
};
```

## 🎯 Component Guide

### Using the Activity Tracker

```javascript
import { useActivity } from '../../context/ActivityContext';

export default function MyComponent() {
  const { addActivity } = useActivity();
  
  // Log activity
  addActivity({
    type: 'competitor_analysis',
    title: 'Competitor Analysis Completed',
    description: 'Analyzed Lyft'
  });
}
```

### Activity Types

- `competitor_analysis` - Competitor analysis completed
- `video_analysis` - Video pitch analyzed
- `pdf_analysis` - PDF document analyzed
- `document_upload` - Document uploaded to RAG
- `rag_query` - Question asked in Ask Your Startup

## 🎨 Design System

### Colors

The app uses a custom design system with CSS variables:

```css
--color-primary: #21808d (Teal 500)
--color-background: #fcfcf9 (Cream 50)
--color-text: #134252 (Slate 900)
```

### Components

All UI components follow consistent patterns:

- **Button**: `variant` (primary, secondary, outline), `size` (sm, md, lg)
- **Card**: `CardHeader`, `CardBody` for structured content
- **Inputs**: Consistent styling with focus states

### Dark Mode

Automatic dark mode support using CSS media queries:

```css
@media (prefers-color-scheme: dark) {
  --color-background: #1f2121;
  --color-text: #f5f5f5;
}
```

## 🚀 Building for Production

```bash
# Build for production
npm run build

# Preview production build
npm run preview

# The build output will be in the dist/ folder
```

### Deployment

The app can be deployed to:

- **Vercel** (recommended)
- **Netlify**
- **AWS S3 + CloudFront**
- **Google Cloud Storage**

Example Vercel deployment:

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

## 📊 Performance

- **Code Splitting**: Automatic route-based code splitting
- **Lazy Loading**: Components loaded on demand
- **Optimized Images**: Use WebP format when possible
- **Caching**: TanStack Query handles data caching

## 🧪 Testing

```bash
# Run tests (if configured)
npm test

# Run linting
npm run lint
```

## 🐛 Troubleshooting

### Common Issues

**CORS Errors**
- Ensure backend has CORS enabled for your frontend URL
- Check `VITE_API_BASE_URL` is correct

**API Connection Failed**
- Verify backend is running
- Check network tab in browser DevTools
- Ensure environment variables are loaded

**Dark Mode Issues**
- Clear browser cache
- Check CSS variables are loading

**Table Rendering Issues**
- Ensure backend returns data in correct format (arrays)
- Check browser console for errors

## 📚 Documentation

### Key Files to Review

- `ActivityContext.jsx` - Activity tracking implementation
- `AIAnalyzer.jsx` - PDF analysis with tabs
- `AskYourStartup.jsx` - RAG chat interface
- `CompetitorAnalysis.jsx` - Competitor analysis

### API Response Formats

See individual component files for expected API response structures.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Use functional components with hooks
- Follow ESLint configuration
- Use Tailwind for styling
- Add comments for complex logic

## 📄 License

This project is licensed under the MIT License.

## 🏆 Hackathon Submission

### Technical Merit (50%)
✅ Full working build end-to-end
✅ Edge case handling (unparsable tables, empty results)
✅ Google AI tools integration (Gemini, Document AI, Video AI)
✅ Scalable architecture (React + Context + TanStack Query)

### User Experience (10%)
✅ Intuitive dashboard interface
✅ Mobile-responsive design
✅ Clear feedback and loading states
✅ Accessible UI components

### Alignment with Cause (10%)
✅ Solves real startup pain point (fragmented information)
✅ Accelerates decision-making for founders and VCs
✅ Positive impact on startup ecosystem

### Innovation & Creativity (20%)
✅ All-in-one platform approach
✅ Multiple data sources (web, video, PDF)
✅ RAG-powered document Q&A
✅ Real-time activity tracking

### Market Feasibility (10%)
✅ Clear target market (startup founders, VCs, analysts)
✅ SaaS business model ready
✅ Low barrier to entry (web-based)
✅ Scalable architecture


Built with ❤️ for the Google AI Hackathon

