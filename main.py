from fastapi import FastAPI, Path, Query
from pydantic import BaseModel

app = FastAPI()


class Note(BaseModel):
    name: str
    description: str
    done: bool


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI!"}

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# @app.get("/note/new")
# async def read_new_notes():
#     return {"message": "Return new notes"}

# @app.get("/notes/{note_id}")
# # async def read_note(note_id: int):
# async def read_note(note_id: int = Path(description="The ID of the note to get", gt=0, le=10)):
#     return {"note": note_id}

@app.get("/notes")
# async def read_notes(skip: int = 0, limit: int = 10):
# async def read_notes(skip: int = 0, limit: int = 10, q: str | None = None):
async def read_notes(skip: int = 0, limit: int = Query(default=10, le=100, ge=10)):
    return {"message": f"Return all notes: skip: {skip}, limit: {limit}"}

@app.post("/notes")
async def create_note(note: Note):
    return {"name": note.name, "description": note.description, "status": note.done}
