from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import order_controller, product_controller, restaurant_controller
from app.models.common_model import Base
from app.db.connection import engine

app = FastAPI()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(restaurant_controller.router)
app.include_router(product_controller.router)
app.include_router(order_controller.router)


@app.on_event("shutdown")
async def shutdown_event():
    pass


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
