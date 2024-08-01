import time
import pathlib

from fastapi import FastAPI, Path, Query, Depends, HTTPException, status, Request, File, UploadFile
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.orm import Session

from db import get_db, Note

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


# class Note(BaseModel):
#     name: str
#     description: str
#     done: bool

class ResponseNoteModel(BaseModel):
    id: int = Field(default=1, ge=1)
    name: str
    description: str
    done: bool


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/api/healthchecker")
# def root():
#     return {"message": "Welcome to FastAPI!"}
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        # result = db.execute("SELECT 1").fetchone()  # Error connecting to the database
        result = db.execute(text("SELECT 1")).fetchone()  # Welcome to FastAPI!
        if result is None:
            # raise HTTPException(status_code=500, detail="Database is not configured correctly")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        # raise HTTPException(status_code=500, detail="Error connecting to the database")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error connecting to the database")

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# @app.get("/note/new")
# async def read_new_notes():
#     return {"message": "Return new notes"}

@app.get("/notes")
# async def read_notes(skip: int = 0, limit: int = 10):
# async def read_notes(skip: int = 0, limit: int = 10, q: str | None = None):
# async def read_notes(skip: int = 0, limit: int = Query(default=10, le=100, ge=10)):
async def read_notes(skip: int = 0, limit: int = Query(default=10, le=100, ge=10), db: Session = Depends(get_db)) -> list[ResponseNoteModel]:
    notes = db.query(Note).offset(skip).limit(limit).all()
    # return {"message": f"Return all notes: skip: {skip}, limit: {limit}"}
    return notes

@app.get("/notes/{note_id}", response_model=ResponseNoteModel)
# # async def read_note(note_id: int):
# async def read_note(note_id: int = Path(description="The ID of the note to get", gt=0, le=10)):
async def read_note(note_id: int = Path(description="The ID of the note to get", gt=0, le=10), db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return note
#     return {"note": note_id}

# @app.post("/notes")
# async def create_note(note: Note):
#     return {"name": note.name, "description": note.description, "status": note.done}

class NoteModel(BaseModel):
    name: str
    description: str
    done: bool


@app.post("/notes")
async def create_note(note: NoteModel, db: Session = Depends(get_db)):
    new_note = Note(name=note.name, description=note.description, done=note.done)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File()):
    pathlib.Path("uploads").mkdir(exist_ok=True)
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"file_path": file_path}
