#!/usr/bin/env python3
"""
PostgreSQL setup script for EmpowerLex
"""
import os
import sys
import subprocess
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_postgres_installation():
    """Check if PostgreSQL is installed"""
    try:
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"PostgreSQL found: {result.stdout.strip()}")
            return True
        else:
            logger.error("PostgreSQL not found")
            return False
    except FileNotFoundError:
        logger.error("PostgreSQL not installed")
        return False

def create_database_and_user():
    """Create database and user for EmpowerLex"""
    try:
        # Create user
        logger.info("Creating PostgreSQL user...")
        subprocess.run([
            'sudo', '-u', 'postgres', 'psql', '-c',
            "CREATE USER empowerlex WITH PASSWORD 'empowerlex_password';"
        ], check=True)
        
        # Create database
        logger.info("Creating PostgreSQL database...")
        subprocess.run([
            'sudo', '-u', 'postgres', 'psql', '-c',
            "CREATE DATABASE empowerlex OWNER empowerlex;"
        ], check=True)
        
        # Grant privileges
        logger.info("Granting privileges...")
        subprocess.run([
            'sudo', '-u', 'postgres', 'psql', '-c',
            "GRANT ALL PRIVILEGES ON DATABASE empowerlex TO empowerlex;"
        ], check=True)
        
        logger.info("Database and user created successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Error creating database: {e}")
        return False

def create_env_file():
    """Create .env file with PostgreSQL configuration"""
    env_content = """# Database Configuration
DATABASE_URL=postgresql://empowerlex:empowerlex_password@localhost:5432/empowerlex

# PostgreSQL specific settings
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=empowerlex
POSTGRES_PASSWORD=empowerlex_password
POSTGRES_DB=empowerlex

# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# JWT Settings
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# App Settings
DEBUG=True
APP_NAME=Legal Aid Platform
"""
    
    env_file = Path('.env')
    if env_file.exists():
        logger.warning(".env file already exists. Backing up...")
        env_file.rename('.env.backup')
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    logger.info(".env file created successfully!")

def install_dependencies():
    """Install PostgreSQL dependencies"""
    try:
        logger.info("Installing PostgreSQL dependencies...")
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', 'psycopg2-binary'
        ], check=True)
        logger.info("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error installing dependencies: {e}")
        return False

def main():
    """Main setup function"""
    logger.info("Setting up PostgreSQL for EmpowerLex...")
    
    # Check PostgreSQL installation
    if not check_postgres_installation():
        logger.error("Please install PostgreSQL first:")
        logger.error("Ubuntu/Debian: sudo apt-get install postgresql postgresql-contrib")
        logger.error("macOS: brew install postgresql")
        logger.error("Windows: Download from https://www.postgresql.org/download/windows/")
        return
    
    # Install Python dependencies
    if not install_dependencies():
        return
    
    # Create database and user
    if not create_database_and_user():
        return
    
    # Create .env file
    create_env_file()
    
    logger.info("PostgreSQL setup completed!")
    logger.info("Next steps:")
    logger.info("1. Update the .env file with your actual API keys")
    logger.info("2. Run: alembic upgrade head")
    logger.info("3. Run: python scripts/migrate_to_postgres.py (if migrating from SQLite)")
    logger.info("4. Start your application")

if __name__ == "__main__":
    main() 