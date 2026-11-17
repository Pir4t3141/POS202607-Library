from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi_restful.cbv import cbv
from pydantic import BaseModel, field_validator, ValidationError, Field
from sqlalchemy.orm import Session
from starlette import status

import json_helper
from routers.base import BaseAPI

router = APIRouter(prefix="/books", tags=["Books"])

# Pydentic Schemas

class BookCreate(BaseModel):
    isbn:str = Field(...)
    title:str = Field(...)
    author:str = Field(...)
    publisher:str = Field(...)
    published_year:int = Field(serialization_alias='publishedYear')
    is_available:bool = Field(default=True, serialization_alias='isAvailable')

    @field_validator('isbn')
    @classmethod
    def check_is_correct_len(cls, value:str):
        if len(value) == 10 or len(value) == 13:
            return value
        else:
            raise ValueError('ISBN must be 10 or 13 digits')

class BookResponse(BookCreate):
    id: int

@cbv(router)
class ItemAPI(BaseAPI):

    # TODO: Change to DB

    @router.get("/", response_model=list[BookResponse])
    def get_books(self):
        return [BookResponse.model_validate_json(book) for book in json_helper.get_all_books()]

    @router.get("/{book_id}", response_model=BookResponse)
    def get_book_by_id(self, book_id:int):
        return BookResponse.model_validate_json(json_helper.get_book_by_id(book_id))

    @router.get("/", response_model=list[BookResponse])
    def get_books_by_title(self, title:str):
        ...
        # TODO: Search by title

    @router.post("/")
    def create_book(self, book:BookCreate):
        bookRes = BookResponse(**book.model_dump(), id=json_helper.get_id_for_next_book())
        raise json_helper.add_book(bookRes)

    @router.delete("/{book_id}")
    def delete_book(self, book_id:int):
        book = self.get_or_404(self.db, models.DBbook, book_id)

        if book is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="book not found")

        self.db.delete(book)
        self.db.commit()

        raise HTTPException(status_code=status.HTTP_200_OK, detail="book deleted")