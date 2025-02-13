from typing import List
import strawberry
from strawberry.fastapi import GraphQLRouter
from app.models.database import get_db
from app.models.models import Book, Review
import asyncio

# GraphQL schema
@strawberry.type
class BookType:
    id: int
    title: str
    author: str

@strawberry.type
class ReviewType:
    id: int
    book_id: int
    rating: int
    comment: str

@strawberry.type
class Query:
    @strawberry.field
    def get_books(self) -> List[Book]:  
        with get_db() as db:
            books = db.query(Book).all()
            return [BookType(id=book.id, title=book.title, author=book.author) for book in books]

    @strawberry.field
    def get_book(self, book_id: int) -> BookType:
        with get_db() as db:
            book = db.query(Book).filter(Book.id == book_id).first()
            return BookType(id=book.id, title=book.title, author=book.author)   

    @strawberry.field
    def get_reviews(self, book_id: int) -> List[ReviewType]:
        with get_db() as db:
            reviews = db.query(Review).filter(Review.book_id == book_id).all()
            return [ReviewType(id=review.id, rating=review.rating, comment=review.comment) for review in reviews]

    @strawberry.field
    def get_review(self, book_id: int, review_id: int) -> ReviewType:
        with get_db() as db:
            review = db.query(Review).filter(Review.id == review_id).first()
            return ReviewType(id=review.id, rating=review.rating, comment=review.comment)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_book(self, title: str, author: str) -> BookType:
        with get_db() as db:
            db_book = Book(title=title, author=author)
            db.add(db_book)
            db.commit()
            db.refresh(db_book)
            return BookType(id=db_book.id, title=db_book.title, author=db_book.author)

    @strawberry.mutation
    def update_book(self, book_id: int, title: str, author: str) -> BookType:
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
    def delete_book(self, book_id: int) -> BookType:
        with get_db() as db:
            db_book = db.query(Book).filter(Book.id == book_id).first()
            if db_book:
                db.delete(db_book)
                db.commit()
                return BookType(id=db_book.id, title=db_book.title, author=db_book.author)
            else:
                raise Exception("Book not found")

    @strawberry.mutation
    def create_review(self, book_id: int, rating: int, comment: str) -> ReviewType:
        with get_db() as db:
            db_review = Review(book_id=book_id, rating=rating, comment=comment)
            db.add(db_review)
            db.commit()
            db.refresh(db_review)
            return ReviewType(id=db_review.id, rating=db_review.rating, comment=db_review.comment)  

    @strawberry.mutation
    def update_review(self, book_id: int, review_id: int, rating: int, comment: str) -> ReviewType:
        with get_db() as db:
            db_review = db.query(Review).filter(Review.id == review_id).first()
            if db_review:
                db_review.rating = rating
                db_review.comment = comment
                db.commit()
                db.refresh(db_review)
                return ReviewType(id=db_review.id, rating=db_review.rating, comment=db_review.comment)
            else:
                raise Exception("Review not found")

    @strawberry.mutation
    def delete_review(self, book_id: int, review_id: int) -> bool:
        with get_db() as db:
            db_review = db.query(Review).filter(Review.id == review_id).first()
            if db_review:
                db.delete(db_review)
                db.commit()
                return True
            else:
                raise Exception("Review not found")

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)