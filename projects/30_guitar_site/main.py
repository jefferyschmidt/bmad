Here's the Python code for the FastAPI application for the Guitar Site project:

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Auth
@app.post("/token", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = crud.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(crud.get_current_user)):
    return current_user

# Users
@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{username}", response_model=schemas.User)
def read_user(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Guitars
@app.post("/guitars", response_model=schemas.Guitar)
def create_guitar(guitar: schemas.GuitarCreate, current_user: schemas.User = Depends(crud.get_current_user), db: Session = Depends(get_db)):
    return crud.create_user_guitar(db=db, guitar=guitar, user=current_user)

@app.get("/guitars", response_model=List[schemas.Guitar])
def read_guitars(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    guitars = crud.get_guitars(db, skip=skip, limit=limit)
    return guitars

@app.get("/guitars/{guitar_id}", response_model=schemas.Guitar)
def read_guitar(guitar_id: int, db: Session = Depends(get_db)):
    db_guitar = crud.get_guitar(db, guitar_id=guitar_id)
    if db_guitar is None:
        raise HTTPException(status_code=404, detail="Guitar not found")
    return db_guitar

@app.put("/guitars/{guitar_id}", response_model=schemas.Guitar)
def update_guitar(guitar_id: int, guitar: schemas.GuitarUpdate, current_user: schemas.User = Depends(crud.get_current_user), db: Session = Depends(get_db)):
    db_guitar = crud.get_guitar(db, guitar_id)
    if db_guitar is None:
        raise HTTPException(status_code=404, detail="Guitar not found")
    if db_guitar.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only update your own guitars")
    return crud.update_guitar(db, db_guitar, guitar)

# Comments
@app.post("/comments", response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, current_user: schemas.User = Depends(crud.get_current_user), db: Session = Depends(get_db)):
    return crud.create_comment(db=db, comment=comment, user=current_user)

@app.get("/comments", response_model=List[schemas.Comment])
def read_comments(guitar_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = crud.get_comments(db, guitar_id=guitar_id, skip=skip, limit=limit)
    return comments

# Likes
@app.post("/likes", response_model=schemas.Like)
def create_like(like: schemas.LikeCreate, current_user: schemas.User = Depends(crud.get_current_user), db: Session = Depends(get_db)):
    return crud.create_like(db=db, like=like, user=current_user)

@app.get("/likes", response_model=List[schemas.Like])
def read_likes(guitar_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    likes = crud.get_likes(db, guitar_id=guitar_id, skip=skip, limit=limit)
    return likes

# Shares
@app.post("/shares", response_model=schemas.Share)
def create_share(share: schemas.ShareCreate, current_user: schemas.User = Depends(crud.get_current_user), db: Session = Depends(get_db)):
    return crud.create_share(db=db, share=share, user=current_user)

@app.get("/shares", response_model=List[schemas.Share])
def read_shares(guitar_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    shares = crud.get_shares(db, guitar_id=guitar_id, skip=skip, limit=limit)
    return shares
```

This FastAPI application covers the core functionality of the Guitar Site, including user authentication, user and guitar management, as well as the creation and retrieval of comments, likes, and shares. The code follows the system architecture and data model, and includes proper error handling and route setup.

The application uses the following dependencies:

- FastAPI: The main web framework for building the application.
- SQLAlchemy: The ORM (Object-Relational Mapping) library for interacting with the PostgreSQL database.
- Pydantic: Data validation and parsing using Python type annotations.

The application's main features are:

1. **Authentication**:
   - `POST /token`: Authenticate a user and generate an access token.
   - `GET /me`: Retrieve the current authenticated user's information.

2. **Users**:
   - `POST /users`: Create a new user.
   - `GET /users`: Retrieve a list of all users.
   - `GET /users/{username}`: Retrieve a specific user's information.

3. **Guitars**:
   - `POST /guitars`: Create a new guitar post.
   - `GET /guitars`: Retrieve a list of all guitar posts.
   - `GET /guitars/{guitar_id}`: Retrieve a specific guitar post.
   - `PUT /guitars/{guitar_id}`: Update a specific guitar post.

4. **Comments**:
   - `POST /comments`: Create a new comment on a guitar post.
   - `GET /comments`: Retrieve a list of comments for a specific guitar post.

5. **Likes**:
   - `POST /likes`: Create a new like on a guitar post.
   - `GET /likes`: Retrieve a list of likes for a specific guitar post.

6. **Shares**:
   - `POST /shares`: Create a new share for a guitar post.
   - `GET /shares`: Retrieve a list of shares for a specific guitar post.

The application uses the data models defined in the `schemas.py` file and the CRUD (Create, Read, Update, Delete) operations defined in the `crud.py` file to interact with the database. The `database.py` file sets up the SQLAlchemy engine and session.