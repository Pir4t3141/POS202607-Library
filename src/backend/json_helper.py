import json
from fastapi import HTTPException
from starlette import status

with open("data/04-01_library_testdata_v2.json", "r") as file:
    data = json.load(file)

def get_all_books():
    return data["books"]

def get_book_by_id(book_id: int):
    return data["books"].where("id", book_id).first()

def get_books_matching_title(title: str):
    return data["books"].where("title")

def get_id_for_next_book() -> int:
    # Source - https://stackoverflow.com/a/55077886
    # Posted by Taimoor Ali
    # Retrieved 2026-11-17, License - CC BY-SA 4.0
    max_id = max(data["books"], key=lambda i: i['id'])
    return int(max_id +1)

def add_book(book_dict: dict) -> HTTPException:
    try:
        with open("data/04-01_library_testdata_v2.json", "a") as file_r:
            file_r.write(json.dumps(book_dict))
            return  HTTPException(status_code=status.HTTP_201_CREATED, detail="Book Added")
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to add Book.\nMore Details: {e}")
