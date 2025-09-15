# Influencer Search Platform

A comprehensive AI-powered influencer discovery and outreach platform that helps companies find, analyze, and contact the perfect YouTube influencers for their products.

## 🚀 Features

### Core Functionality
- **Company Registration**: Register companies with automatic brand analysis from website scraping
- **Product Management**: Add products with detailed categorization and targeting
- **AI-Powered Influencer Search**: Find YouTube influencers using advanced algorithms
- **Smart Fit Scoring**: Multi-factor analysis including content alignment, audience demographics, and brand values
- **Dynamic Pricing**: Intelligent pricing based on CPM, engagement rates, and market data
- **Automated Outreach**: Personalized email campaigns with AI-generated content
- **Campaign Management**: Track and manage influencer relationships

### AI & Analytics
- **Brand Analysis**: GPT-4 powered website analysis for brand understanding
- **Content Categorization**: Automatic classification of influencer content
- **Audience Demographics**: AI-driven audience analysis and targeting
- **Fit Scoring Algorithm**: Sophisticated matching based on multiple factors
- **ROI Estimation**: Predictive analytics for campaign success

## 🛠 Tech Stack

- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.8+, SQLAlchemy
- **Database**: SQLite (development), PostgreSQL (production ready)
- **AI/ML**: OpenAI GPT-4, Custom algorithms
- **APIs**: YouTube Data API v3, SMTP
- **UI/UX**: Lucide React icons, Responsive design

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- OpenAI API key
- YouTube Data API v3 key
- Gmail account with app password (for email outreach)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd influencer_search_full_project
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp env.example .env

# Edit .env file with your API keys
# OPENAI_API_KEY=your_openai_key
# YOUTUBE_API_KEY=your_youtube_key
# EMAIL_USERNAME=your_email@gmail.com
# EMAIL_PASSWORD=your_app_password

# Run the backend server
uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 🔧 API Keys Setup

### OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an account and generate an API key
3. Add the key to your `.env` file

### YouTube Data API v3 Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. Add the key to your `.env` file

### Gmail App Password
1. Enable 2-factor authentication on your Google account
2. Generate an app password for "Mail"
3. Use this password in your `.env` file

## 📱 Usage

### 1. Company Registration
- Enter company name, email, and website URL
- The system automatically scrapes and analyzes your website
- AI extracts brand keywords, target audience, and values

### 2. Product Creation
- Add product details including name, description, and category
- Specify price range for better targeting
- Products are linked to your company profile

### 3. Influencer Search
- Set search parameters (max results, minimum fit score)
- AI searches YouTube for relevant influencers
- Advanced algorithms analyze content and audience fit

### 4. Review & Contact
- Review influencer profiles with detailed analytics
- Approve or reject individual influencers
- Send automated personalized outreach emails

## 🏗 Architecture

### Backend Structure
```
backend/
├── app/
│   ├── api/
│   │   └── routes.py          # FastAPI routes
│   ├── models/
│   │   └── models.py          # SQLAlchemy models
│   ├── services/
│   │   ├── scrape_brand.py    # Brand analysis service
│   │   ├── youtube_search.py  # YouTube API integration
│   │   └── send_email.py      # Email outreach service
│   ├── utils/
│   │   └── fit_and_pricing.py # AI algorithms
│   └── main.py                # FastAPI application
├── requirements.txt
└── .env
```

### Frontend Structure
```
frontend/
├── pages/
│   └── index.tsx              # Main application page
├── styles/
│   └── globals.css            # Global styles
├── package.json
├── tailwind.config.js
└── next.config.js
```

## 🧠 AI Algorithms

### Fit Scoring Algorithm
The platform uses a sophisticated multi-factor scoring system:

1. **Content Fit (30%)**: Category and keyword matching
2. **Audience Fit (25%)**: Demographic and psychographic alignment
3. **Engagement Fit (20%)**: Quality of audience engagement
4. **Brand Alignment (25%)**: Values and tone matching

### Pricing Algorithm
Dynamic pricing based on:
- Base CPM calculation
- Engagement rate multipliers
- Subscriber count adjustments
- Content category premiums
- Market demand factors

### Brand Analysis
AI-powered website analysis extracts:
- Brand summary and value proposition
- Target audience demographics
- Brand keywords and values
- Content categories and tone
- Unique selling points

## 🔒 Security & Privacy

- Environment variables for sensitive data
- Input validation and sanitization
- Rate limiting on API endpoints
- Secure email handling
- No storage of sensitive influencer data

## 🚀 Deployment

### Backend Deployment
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Start production server
npm start
```

## 📊 Performance

- **Backend**: FastAPI with async/await for high performance
- **Database**: SQLAlchemy with connection pooling
- **Frontend**: Next.js with optimized builds
- **Caching**: Intelligent caching of influencer data
- **Rate Limiting**: API rate limiting to prevent abuse

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support or questions:
- Create an issue in the repository
- Check the documentation
- Review the API endpoints at `http://localhost:8000/docs`

---

Built with ❤️ for Dreamwell AI - Advanced Influencer Marketing Platform
