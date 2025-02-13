from typing import List

from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)

    reviews = relationship("Review", back_populates="book")


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)
    comment = Column(Text)

    book_id = Column(Integer, ForeignKey("books.id"))
    book = relationship("Book", back_populates="reviews")

