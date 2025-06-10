from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.user_schema import UserCreate, UserLogin, UserResponse, Token
from app.auth.utils import verify_password, get_password_hash, create_access_token
from app.auth.dependencies import get_current_active_user
from app.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/signup", response_model=Token)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    print("DEBUG: Signup function called with user:", user)
    print("DEBUG: Database session:", db)
    # Check if user already exists
    try:
        db_user = db.query(User).filter(
            (User.email == user.email) | (User.username == user.username)
        ).first()
        print("DEBUG: Query executed successfully")
    except Exception as e:
        print("DEBUG: Database query error:", str(e))
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")
    
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email or username already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    print("DEBUG: Creating user with data:", {
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "phone": user.phone,
        "location": user.location,
        "hashed_password": hashed_password
    })
    try:
        print("DEBUG: About to create User object")
        db_user = User(
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            phone=user.phone,
            location=user.location,
            hashed_password=hashed_password
        )
        print("DEBUG: User object created successfully:", db_user)
        print("DEBUG: About to add user to database")
        db.add(db_user)
        print("DEBUG: About to commit transaction")
        db.commit()
        print("DEBUG: About to refresh user object")
        db.refresh(db_user)
        print("DEBUG: User object refreshed successfully")
    except Exception as e:
        print("DEBUG: Database error:", str(e))
        logger.error(f"Signup error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(db_user)
    }

@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return access token"""
    try:
        user = db.query(User).filter(User.username == user_credentials.username).first()
        
        if not user or not verify_password(user_credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse.from_orm(user)
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user
