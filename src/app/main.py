from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import notes, ping
from app.db import engine, metadata, database


metadata.create_all(engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])


if __name__ == "__main__":
   # pipenv run uvicorn app.main:app --reload
    uvicorn.run(app, host="localhost", port=8000)

