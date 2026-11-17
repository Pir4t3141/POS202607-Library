from fastapi import HTTPException
from sqlalchemy.orm import Session

# Used for shared functions between the routers

class BaseAPI:

    def get_or_404(self, db: Session, item_id: int):
        ...
        # TODO: Change to get from DB (add model: Base)
