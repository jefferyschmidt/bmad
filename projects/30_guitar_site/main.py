Here's the Python FastAPI application file for the "Guitar Site" project:

```python
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from passlib.context import CryptContext
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

from . import models, schemas
from .database import SessionLocal, engine

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = db.query(models.User).filter(models.User.username == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# User Management
@app.post("/users/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/users/login", response_model=schemas.Token)
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/{username}", response_model=schemas.UserResponse)
def get_user_profile(username: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{username}/update", response_model=schemas.UserResponse)
def update_user_profile(
    username: str,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.username != username:
        raise HTTPException(
            status_code=403, detail="You are not authorized to update this profile."
        )
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.profile_picture = user_update.profile_picture
    db_user.bio = user_update.bio
    db_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return db_user

# Guitar Management
@app.post("/guitars/create", response_model=schemas.GuitarResponse)
def create_guitar(
    guitar: schemas.GuitarCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_guitar = models.Guitar(
        user_id=current_user.user_id,
        brand=guitar.brand,
        model=guitar.model,
        year=guitar.year,
        description=guitar.description,
        guitar_photos=guitar.guitar_photos,
    )
    db.add(db_guitar)
    db.commit()
    db.refresh(db_guitar)
    return db_guitar

@app.get("/guitars/{guitar_id}", response_model=schemas.GuitarResponse)
def get_guitar(guitar_id: int, db: Session = Depends(get_db)):
    db_guitar = db.query(models.Guitar).filter(models.Guitar.guitar_id == guitar_id).first()
    if db_guitar is None:
        raise HTTPException(status_code=404, detail="Guitar not found")
    return db_guitar

@app.put("/guitars/{guitar_id}/update", response_model=schemas.GuitarResponse)
def update_guitar(
    guitar_id: int,
    guitar_update: schemas.GuitarUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_guitar = db.query(models.Guitar).filter(models.Guitar.guitar_id == guitar_id).first()
    if db_guitar is None:
        raise HTTPException(status_code=404, detail="Guitar not found")
    if db_guitar.user_id != current_user.user_id:
        raise HTTPException(
            status_code=403, detail="You are not authorized to update this guitar."
        )
    db_guitar.brand = guitar_update.brand
    db_guitar.model = guitar_update.model
    db_guitar.year = guitar_update.year
    db_guitar.description = guitar_update.description
    db_guitar.guitar_photos = guitar_update.guitar_photos
    db_guitar.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_guitar)
    return db_guitar

# Interaction and Engagement
@app.post("/comments/create", response_model=schemas.CommentResponse)
def create_comment(
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_comment = models.Comment(
        guitar_id=comment.guitar_id,
        user_id=current_user.user_id,
        comment_text=comment.comment_text,
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@app.post("/likes/create", response_model=schemas.LikeResponse)
def create_like(
    like: schemas.LikeCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_like = models.Like(
        guitar_id=like.guitar_id,
        user_id=current_user.user_id,
    )
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like

@app.post("/shares/create", response_model=schemas.ShareResponse)
def create_share(
    share: schemas.ShareCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_share = models.Share(
        guitar_id=share.guitar_id,
        user_id=current_user.user_id,
    )
    db.add(db_share)
    db.commit()
    db.refresh(db_share)
    return db_share

# Content Delivery
@app.get("/profiles", response_model=List[schemas.UserResponse])
def get_public_profiles(db: Session = Depends(get_db)):
    db_users = db.query(models.User).all()
    return db_users

@app.get("/profiles/{username}", response_model=schemas.UserResponse)
def get_public_profile(username: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/guitars/search", response_model=List[schemas.GuitarResponse])
def search_guitars(
    brand: str = None,
    model: str = None,
    year: int = None,
    db: Session = Depends(get_db),
):
    db_guitars = db.query(models.Guitar)
    if brand:
        db_guitars = db_guitars.filter(models.Guitar.brand.ilike(f"%{brand}%"))
    if model:
        db_guitars = db_guitars.filter(models.Guitar.model.ilike(f"%{model}%"))
    if year:
        db_guitars = db_guitars.filter(models.Guitar.year == year)
    return db_guitars.all()
```

This code includes the following:

1. Proper error handling with `HTTPException`.
2. Route setup for user management, guitar management, interaction and engagement, and content delivery.
3. Basic endpoints for user registration, login, profile retrieval and update, guitar creation, retrieval, and update, as well as commenting, liking, and sharing functionality.
4. Database models and schemas based on the provided data model.
5. Implementation of JWT-based authentication and authorization using the `get_current_user` function.
6. Dependency injection for the database session using `get_db`.
7. Password hashing and verification using the `passlib` library.

The code follows the system architecture and UX design specifications provided in the earlier sections.