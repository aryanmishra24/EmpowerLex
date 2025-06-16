# EmpowerLex

EmpowerLex is a legal empowerment platform that helps users navigate the legal system by providing personalized legal guidance, connecting them with relevant NGOs, and generating legal documents using advanced AI capabilities.

## Features

- **AI-Powered Legal Assistance**: Get personalized legal guidance using LangChain and OpenAI
- **Case Management**: Create and track legal cases
- **Legal Document Generation**: Generate personalized legal drafts using AI
- **NGO Finder**: Connect with relevant legal aid organizations
- **Case Filtering**: Filter cases by status and category
- **User Authentication**: Secure login and registration system
- **Smart Legal Agent**: AI-powered agent for handling complex legal queries

## Tech Stack

- **Frontend**: Flutter
- **Backend**: Python (FastAPI)
- **Database**: PostgreSQL
- **Authentication**: JWT
- **API**: RESTful
- **AI/ML**: 
  - LangChain
  - Gemini
  - Custom AI Agents

## Project Structure

```
empower_lex/
├── app/                    # FastAPI backend
│   ├── api/               # API endpoints
│   ├── models/            # Database models
│   ├── routes/            # Route handlers
│   ├── services/          # Business logic
│   ├── agent/             # AI agent implementation
│   ├── auth/              # Authentication logic
│   ├── scripts/           # Utility scripts
│   └── utils/             # Utility functions
├── empower_lex_mobile/    # Flutter mobile app
├── migrations/            # Database migrations
├── tests/                 # Test suite
└── docs/                  # Documentation
```

## Getting Started

### Prerequisites

- Flutter SDK
- Python 3.8+
- PostgreSQL
- Node.js (for development tools)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/aryanmishra24/empowerLex.git
   cd empowerLex
   ```

2. Set up the backend:
   ```bash
   cd app
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up the mobile app:
   ```bash
   cd empoweLex_mobile
   flutter pub get
   ```

4. Configure API Keys:
   - Create a `.env` file in the root directory
   - Add your API keys:
     ```bash
     GEMINI_API_KEY=your_gemini_api_key_here
     OPENAI_API_KEY=your_openai_api_key_here
     ```

### Running the Application

1. Start the backend server:
   ```bash
   cd app
   uvicorn main:app --reload
   ```

2. Run the mobile app:
   ```bash
   cd empowerLex_mobile
   flutter run
   ```

## AI Features

The platform leverages advanced AI capabilities through:

1. **LangChain Integration**: For building and managing AI workflows
2. **OpenAI Integration**: For natural language processing and document generation
3. **Custom AI Agent**: A specialized agent for handling legal queries and document generation
4. **Smart Document Analysis**: AI-powered analysis of legal documents and case files

## Deployment

### Backend Deployment
1. Set up your API keys in the production environment
2. Configure your database connection
3. Set up SSL/TLS certificates
4. Configure your web server (Nginx/Apache)
5. Set up proper logging and monitoring
6. Configure AI service endpoints and rate limits

### Mobile App Deployment
1. Generate release builds
2. Configure app signing
3. Deploy to app stores

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


