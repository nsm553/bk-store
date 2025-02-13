from typing import List
from fastapi import HTTPException
from app.models.models import Book, Review
from app.models.schema import BookModel, ReviewModel
from fastapi import APIRouter
from app.database.database import SessionLocal
from fastapi.encoders import jsonable_encoder

router = APIRouter()
db = SessionLocal()

@router.get("/books", response_model=List[BookModel])
async def get_books():
    books = db.query(Book).all()
    return [BookModel(id=book.id, title=book.title, author=book.author) for book in books]

@router.get("/books/{book_id}", response_model=BookModel)
async def get_book(book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        return BookModel(id=book.id, title=book.title, author=book.author)
    else:
        raise HTTPException(status_code=404, detail="Book not found")

@router.post("/books", response_model=BookModel)
async def create_book(book: BookModel):
    db_book = Book(title=book.title, author=book.author)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return BookModel(id=db_book.id, title=db_book.title, author=db_book.author)

@router.put("/books/{book_id}", response_model=BookModel)
async def update_book(book_id: int, book: BookModel):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        db_book.title = book.title
        db_book.author = book.author
        db.commit()
        db.refresh(db_book)
        return BookModel(id=db_book.id, title=db_book.title, author=db_book.author)
    else:
        raise HTTPException(status_code=404, detail="Book not found")   

@router.delete("/books/{book_id}", response_model=bool)
async def delete_book(book_id: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    else:
        raise HTTPException(status_code=404, detail="Book not found")

@router.get("/books/{book_id}/reviews", response_model=List[ReviewModel])
async def get_reviews(book_id: int):
    reviews = db.query(Review).filter(Review.book_id == book_id).all()
    return [ReviewModel(id=review.id, rating=review.rating, comment=review.comment) for review in reviews]

@router.post("/books/{book_id}/reviews", response_model=ReviewModel)
async def create_review(book_id: int, review: ReviewModel):
    db_review = Review(book_id=book_id, rating=review.rating, comment=review.comment)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return ReviewModel(id=db_review.id, rating=db_review.rating, comment=db_review.comment)

@router.put("/books/{book_id}/reviews/{review_id}", response_model=ReviewModel)
async def update_review(book_id: int, review_id: int, review: ReviewModel):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review:
        db_review.rating = review.rating
        db_review.comment = review.comment
        db.commit()
        db.refresh(db_review)
        return ReviewModel(id=db_review.id, rating=db_review.rating, comment=db_review.comment)
    else:
        raise HTTPException(status_code=404, detail="Review not found")

@router.delete("/books/{book_id}/reviews/{review_id}", response_model=bool)
async def delete_review(book_id: int, review_id: int):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if db_review:
        db.delete(db_review)
        db.commit()
        return True
    else:
        raise HTTPException(status_code=404, detail="Review not found")

