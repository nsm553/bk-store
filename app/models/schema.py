from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class BookModel:
    id: Optional[int] = None
    title: str = field(default_factory=str)
    author: str = field(default_factory=str)

@dataclass
class ReviewModel:
    id: Optional[int] = None
    book_id: int = field(default_factory=int)
    rating: int = field(default_factory=int)
    comment: str = field(default_factory=str)
