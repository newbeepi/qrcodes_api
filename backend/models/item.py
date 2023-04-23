from sqlalchemy import Column, Integer, String, DECIMAL

from ..database import Base


class Item(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, default="")
    price = Column(DECIMAL(precision=2), nullable=False)
    image = Column(String, nullable=False, default=name+".png")
