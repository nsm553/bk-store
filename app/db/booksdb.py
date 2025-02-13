from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# DB path
SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example of executing a query
with Session(engine) as session:
    result = session.execute(text("SELECT 1")).scalar()
    print(result) # Output: 1