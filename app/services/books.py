from typing import List
import strawberry
from strawberry.types import Info
from fastapi import FastAPI
from strawberry.asgi import GraphQL
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# Database setup
DATABASE_URL = "sqlite:///./books.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GraphQL schema
@strawberry.type
class BookType:
    id: int
    title: str
    author: str

@strawberry.type
class Query:
    @strawberry.field
    def get_books(self, info: Info) -> List[BookType]:
        with get_db() as db:
            books = db.query(Book).all()
            return [BookType(id=book.id, title=book.title, author=book.author) for book in books]
    
    @strawberry.field
    def get_book(self, info: Info, book_id: int) -> BookType:
        with get_db() as db:
            book = db.query(Book).filter(Book.id == book_id).first()
            return BookType(id=book.id, title=book.title, author=book.author)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_book(self, info: Info, title: str, author: str) -> BookType:
        with get_db() as db:
            db_book = Book(title=title, author=author)
            db.add(db_book)
            db.commit()
            db.refresh(db_book)
            return BookType(id=db_book.id, title=db_book.title, author=db_book.author)
    
    @strawberry.mutation
    def update_book(self, info: Info, book_id: int, title: str, author: str) -> BookType:
        with get_db() as db:
            db_book = db.query(Book).filter(Book.id == book_id).first()
            if db_book:
                db_book.title = title
                db_book.author = author
                db.commit()
                db.refresh(db_book)
                return BookType(id=db_book.id, title=db_book.title, author=db_book.author)
            else:
                raise Exception("Book not found")
    
    @strawberry.mutation
    def delete_book(self, info: Info, book_id: int) -> bool:
         with get_db() as db:
            db_book = db.query(Book).filter(Book.id == book_id).first()
            if db_book:
                db.delete(db_book)
                db.commit()
                return True
            else:
                return False

# FastAPI app setup
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/graphql", graphql_app)