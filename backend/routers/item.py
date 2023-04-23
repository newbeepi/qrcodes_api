from fastapi import APIRouter, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.schemas.item import Item, ItemCreate
from backend.control.item import crud as item_crud

from typing_extensions import Annotated

router = APIRouter(prefix="/items", tags=["items"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=Item)
def add_item(
        name: Annotated[str, Form()],
        description: Annotated[str, Form()],
        price: Annotated[float, Form()],
        image: UploadFile = File(...),
        db: Session = Depends(get_db)

):
    item = ItemCreate(name=name, description=description, price=price)
    new_item = item_crud.create_item(item, image, db)
    return new_item


@router.get("/{item_id}/", response_model=Item)
def get_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    return item_crud.get_item_by_id(db, item_id)


@router.get("/qr/{item_id}/")
def get_item_image(item_id: int, db: Session = Depends(get_db)):
    return FileResponse(item_crud.get_item_by_id(db, item_id).image)



