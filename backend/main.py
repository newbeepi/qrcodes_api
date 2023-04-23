from fastapi import FastAPI

from .models import item as item_models
from .database import engine
from .routers import item

app = FastAPI()

app.include_router(item.router)

item_models.Base.metadata.create_all(bind=engine)




