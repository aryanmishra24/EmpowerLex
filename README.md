# EmpowerLex

EmpowerLex is a legal empowerment platform that helps users navigate the legal system by providing personalized legal guidance, connecting them with relevant NGOs, and generating legal documents.

## Features

- **Case Management**: Create and track legal cases
- **Legal Document Generation**: Generate personalized legal drafts
- **NGO Finder**: Connect with relevant legal aid organizations
- **Case Filtering**: Filter cases by status and category
- **User Authentication**: Secure login and registration system

## Tech Stack

- **Frontend**: Flutter
- **Backend**: Python (FastAPI)
- **Database**: PostgreSQL
- **Authentication**: JWT
- **API**: RESTful

## Project Structure

```
empower_lex/
├── empower_lex_mobile/     # Flutter mobile app
├── empower_lex_backend/    # FastAPI backend
└── docs/                   # Documentation
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
   cd empowerLex_backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up the mobile app:
   ```bash
   cd empoweLex_mobile
   flutter pub get
   ```

4. Configure the application:
   - Copy `.env.example` to `.env`
   - Update the values in `.env` with your sensitive data:
     ```bash
     # Example .env file
     DATABASE_URL=postgresql://user:password@localhost:5432/dbname
     JWT_SECRET_KEY=your-secret-key-here
     OPENAI_API_KEY=your-openai-api-key
     SMTP_USERNAME=your-email@gmail.com
     SMTP_PASSWORD=your-app-specific-password
     ```

### Running the Application

1. Start the backend server:
   ```bash
   cd empowerLex_backend
   uvicorn main:app --reload
   ```

2. Run the mobile app:
   ```bash
   cd empowerLex_mobile
   flutter run
   ```

## Deployment

### Backend Deployment
1. Set up your production environment variables in `.env`
2. Configure your database connection
3. Set up SSL/TLS certificates
4. Configure your web server (Nginx/Apache)
5. Set up proper logging and monitoring

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


