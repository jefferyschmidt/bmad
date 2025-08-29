# BMAD - Business Model AI-Driven Development

A comprehensive AI-powered project management and system design platform that automates the software development lifecycle from requirements analysis to system architecture.

## 🚀 Features

### Core Functionality
- **Project Management**: Create, edit, and archive projects with comprehensive metadata
- **AI-Powered Analysis**: Three specialized AI agents working in sequence
- **Database Integration**: PostgreSQL backend with Neon cloud database support
- **Modern UI**: React-based frontend with Material-UI components

### AI Agents Pipeline

#### 1. Requirements Analyst
- Analyzes project requirements using AI
- Generates refined, actionable specifications
- Creates detailed user stories with acceptance criteria
- Validates requirement sufficiency using AI

#### 2. Data Modeler
- Generates database schemas based on requirements
- Uses AI to design optimal data structures
- Supports multiple database types and patterns

#### 3. Software Architect
- Creates comprehensive system architecture documents
- Designs technology stacks and component architectures
- Generates deployment and implementation plans

### AI Provider Support
- **Anthropic Claude**: Advanced reasoning and analysis
- **OpenAI ChatGPT**: Fast and cost-effective processing
- **Extensible**: Easy to add new AI providers
- **Configurable**: Per-project AI provider selection

## 🏗️ Architecture

### Backend (Python/FastAPI)
- **Framework**: FastAPI with async/await support
- **Database**: SQLAlchemy with async PostgreSQL
- **AI Integration**: Plugin-based provider architecture
- **API**: RESTful endpoints with Pydantic validation

### Frontend (React/TypeScript)
- **Framework**: React 18 with TypeScript
- **UI Library**: Material-UI (MUI) components
- **State Management**: React hooks and context
- **Routing**: React Router for navigation

### Database Schema
- **Projects**: Core project information and metadata
- **AI Providers**: Configuration for different AI services
- **Archived Projects**: Soft delete support for project management

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL database (Neon recommended)

### Backend Setup
```bash
cd bmad
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database and AI provider credentials

# Run database migrations
python -m database

# Update AI provider API keys in the database
# The system creates placeholder API keys that need to be updated
# You can update them directly in the database or through the application

# Start the backend server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd src
npm install
npm start
```

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@host:port/database

# AI Providers
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
```

## 📁 Project Structure

```
bmad/
├── agents/                 # AI agent implementations
│   ├── requirements_analyst.py
│   ├── data_modeler.py
│   └── software_architect.py
├── models.py              # SQLAlchemy database models
├── schemas.py             # Pydantic data validation schemas
├── services.py            # Business logic and AI orchestration
├── main.py                # FastAPI application entry point
├── database.py            # Database connection and migrations
└── requirements.txt       # Python dependencies

src/                       # React frontend
├── components/            # Reusable UI components
├── pages/                 # Application pages
├── types/                 # TypeScript type definitions
└── App.tsx               # Main application component
```

## 🔄 Workflow

1. **Create Project**: Define name, description, and requirements
2. **Select AI Provider**: Choose between Anthropic Claude or OpenAI ChatGPT
3. **Analyze Requirements**: AI generates refined specifications and user stories
4. **Generate Data Model**: AI creates database schema based on requirements
5. **Design Architecture**: AI generates comprehensive system architecture
6. **Iterate**: Update requirements and regenerate any stage as needed

## 🎯 Use Cases

- **Startup MVPs**: Rapidly prototype and design software systems
- **Enterprise Projects**: Standardize requirements and architecture processes
- **Freelance Development**: Professional project documentation and planning
- **Educational**: Learn software design patterns and best practices

## 🚧 Development Status

### ✅ Completed
- Core project management functionality
- Requirements analysis with AI validation
- Data modeling with AI generation
- System architecture with AI design
- Multi-provider AI integration
- Modern responsive UI
- Database persistence and archiving

### 🔄 In Progress
- Enhanced AI agent personas
- Additional AI provider support
- Advanced validation and error handling

### 📋 Planned
- User authentication and project sharing
- Team collaboration features
- Export and documentation generation
- Integration with development tools

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with FastAPI, React, and Material-UI
- AI integration powered by Anthropic Claude and OpenAI
- Database hosted on Neon PostgreSQL
- Inspired by modern software development practices

---

**BMAD** - Where AI meets software architecture, making complex system design accessible to everyone.
