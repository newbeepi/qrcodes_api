import os
import shutil

import sqlalchemy.exc
from sqlalchemy.orm import Session
from fastapi import File

from backend.schemas.item import ItemCreate
from backend.models.item import Item

import pyqrcode


def get_item_by_id(db: Session, item_id: int):
    """
    This method takes db as session and item_id as id of item we want to get and returns item with given id
    :param db:
    :param item_id:
    :return:
    """
    return db.query(Item).filter(Item.id == item_id).first()


def get_item_by_name(db: Session, item_name: str):
    """
    This method takes db as session and item_name as name of item we want to get and returns item with given name
    :param db:
    :param item_name:
    :return:
    """
    return db.query(Item).filter(Item.name == item_name).first()


def save_image(name: str, file: File):
    """
    This method takes name of item and file image and saves it into file system with [item name].png and returns
    path to this file
    :param name:
    :param file:
    :return:
    """
    filename = name + ".png"
    out_file_path = "backend/images/items/" + filename
    try:
        with open(filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        os.rename(filename, out_file_path)
    except FileExistsError:
        os.remove(filename)
    return out_file_path


def create_qrcode(id: int):
    """
    This method takes item id as parameter and generates qr code for links to get item information from and saves
    image of qrcode into folder images/qrcode/[item id].png
    :param id:
    :return:
    """
    url = "/items/{id}".format(id=id)
    qr_url = "/items/qr/{id}".format(id=id)
    qr = pyqrcode.create("\n".join([qr_url, url]))
    qr_code_file = "backend/images/qr_codes/{id}.png".format(id=id)
    qr.png(qr_code_file, scale=8)


def create_item(item: ItemCreate, file: File, db: Session):
    """
    This method takes item as pydantic model ItemCreate with data we want to save item and image we want to add to item
    returns item and id of this item
    :param item:
    :param file:
    :param db:
    :return:
    """
    path_to_image = save_image(item.name, file)  # save image to file system
    try:  # creating new item
        new_item = Item(name=item.name, description=item.description, price=item.price, image=path_to_image)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        create_qrcode(new_item.id)  # generate qr code for this item and save it to file system
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        return get_item_by_name(db, item.name)  # if item with same name already in database return this item
    return new_item
