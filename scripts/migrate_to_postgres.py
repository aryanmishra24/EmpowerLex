#!/usr/bin/env python3
"""
Migration script to transfer data from SQLite to PostgreSQL
"""
import os
import sys
import json
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.config import settings
from app.models.db_models import User, Case, Feedback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_sqlite_engine():
    """Create SQLite engine for reading existing data"""
    sqlite_url = "sqlite:///./app.db"
    return create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_postgres_engine():
    """Create PostgreSQL engine for writing new data"""
    if not settings.database_url.startswith("postgresql"):
        raise ValueError("DATABASE_URL must be a PostgreSQL URL")
    return create_engine(settings.database_url)

def migrate_users(sqlite_engine, postgres_engine):
    """Migrate users from SQLite to PostgreSQL"""
    logger.info("Migrating users...")
    
    # Read from SQLite
    with sqlite_engine.connect() as sqlite_conn:
        users = sqlite_conn.execute(text("SELECT * FROM users")).fetchall()
    
    # Write to PostgreSQL
    with postgres_engine.connect() as postgres_conn:
        for user in users:
            try:
                # Handle JSON fields that might be stored as strings
                postgres_conn.execute(text("""
                    INSERT INTO users (id, username, email, hashed_password, full_name, location, phone, is_active, created_at, updated_at)
                    VALUES (:id, :username, :email, :hashed_password, :full_name, :location, :phone, :is_active, :created_at, :updated_at)
                    ON CONFLICT (id) DO NOTHING
                """), {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'hashed_password': user.hashed_password,
                    'full_name': user.full_name,
                    'location': user.location,
                    'phone': getattr(user, 'phone', None),
                    'is_active': getattr(user, 'is_active', True),
                    'created_at': user.created_at,
                    'updated_at': user.updated_at
                })
            except Exception as e:
                logger.error(f"Error migrating user {user.id}: {e}")
        
        postgres_conn.commit()
    
    logger.info(f"Migrated {len(users)} users")

def migrate_cases(sqlite_engine, postgres_engine):
    """Migrate cases from SQLite to PostgreSQL"""
    logger.info("Migrating cases...")
    
    # Read from SQLite
    with sqlite_engine.connect() as sqlite_conn:
        cases = sqlite_conn.execute(text("SELECT * FROM cases")).fetchall()
    
    # Write to PostgreSQL
    with postgres_engine.connect() as postgres_conn:
        for case in cases:
            try:
                # Convert JSON strings to proper JSONB format
                applicable_laws = json.loads(case.applicable_laws) if case.applicable_laws else None
                suggested_ngos = json.loads(case.suggested_ngos) if case.suggested_ngos else None
                next_steps = json.loads(case.next_steps) if case.next_steps else None
                
                # Generate new UUID for case_id if it doesn't exist
                case_id = case.case_id if case.case_id else None
                
                postgres_conn.execute(text("""
                    INSERT INTO cases (id, case_id, user_id, title, description, category, priority, status, 
                                     generated_draft, applicable_laws, suggested_ngos, next_steps, created_at, updated_at)
                    VALUES (:id, :case_id, :user_id, :title, :description, :category, :priority, :status,
                           :generated_draft, :applicable_laws, :suggested_ngos, :next_steps, :created_at, :updated_at)
                    ON CONFLICT (id) DO NOTHING
                """), {
                    'id': case.id,
                    'case_id': case_id,
                    'user_id': case.user_id,
                    'title': case.title,
                    'description': case.description,
                    'category': case.category,
                    'priority': getattr(case, 'priority', 'medium'),
                    'status': case.status,
                    'generated_draft': case.generated_draft,
                    'applicable_laws': json.dumps(applicable_laws) if applicable_laws else None,
                    'suggested_ngos': json.dumps(suggested_ngos) if suggested_ngos else None,
                    'next_steps': json.dumps(next_steps) if next_steps else None,
                    'created_at': case.created_at,
                    'updated_at': case.updated_at
                })
            except Exception as e:
                logger.error(f"Error migrating case {case.id}: {e}")
        
        postgres_conn.commit()
    
    logger.info(f"Migrated {len(cases)} cases")

def migrate_feedback(sqlite_engine, postgres_engine):
    """Migrate feedback from SQLite to PostgreSQL"""
    logger.info("Migrating feedback...")
    
    # Read from SQLite
    with sqlite_engine.connect() as sqlite_conn:
        feedbacks = sqlite_conn.execute(text("SELECT * FROM feedback")).fetchall()
    
    # Write to PostgreSQL
    with postgres_engine.connect() as postgres_conn:
        for feedback in feedbacks:
            try:
                postgres_conn.execute(text("""
                    INSERT INTO feedback (id, case_id, rating, comments, created_at)
                    VALUES (:id, :case_id, :rating, :comments, :created_at)
                    ON CONFLICT (id) DO NOTHING
                """), {
                    'id': feedback.id,
                    'case_id': feedback.case_id,
                    'rating': feedback.rating,
                    'comments': feedback.comments,
                    'created_at': feedback.created_at
                })
            except Exception as e:
                logger.error(f"Error migrating feedback {feedback.id}: {e}")
        
        postgres_conn.commit()
    
    logger.info(f"Migrated {len(feedbacks)} feedback records")

def main():
    """Main migration function"""
    try:
        logger.info("Starting migration from SQLite to PostgreSQL...")
        
        # Create engines
        sqlite_engine = create_sqlite_engine()
        postgres_engine = create_postgres_engine()
        
        # Test connections
        logger.info("Testing database connections...")
        with sqlite_engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            logger.info(f"SQLite users: {result.scalar()}")
        
        with postgres_engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            logger.info(f"PostgreSQL users: {result.scalar()}")
        
        # Run migrations
        migrate_users(sqlite_engine, postgres_engine)
        migrate_cases(sqlite_engine, postgres_engine)
        migrate_feedback(sqlite_engine, postgres_engine)
        
        logger.info("Migration completed successfully!")
        
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 