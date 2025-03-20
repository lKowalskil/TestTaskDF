from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db
from app.services.ai_service import summarize_text

router = APIRouter()

@router.post("/notes/", response_model=schemas.Note, status_code=status.HTTP_201_CREATED)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_note = models.Note(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    
    note_version = models.NoteVersion(
        note_id=db_note.id,
        title=note.title,
        content=note.content,
        version_number=1
    )
    db.add(note_version)
    db.commit()
    
    return db_note

@router.get("/notes/", response_model=List[schemas.Note])
def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notes = db.query(models.Note).offset(skip).limit(limit).all()
    return notes

@router.get("/notes/{note_id}", response_model=schemas.NoteWithVersions)
def read_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

@router.put("/notes/{note_id}", response_model=schemas.Note)
def update_note(note_id: int, note: schemas.NoteUpdate, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    latest_version = db.query(models.NoteVersion).filter(
        models.NoteVersion.note_id == note_id
    ).order_by(models.NoteVersion.version_number.desc()).first()
    
    new_version_number = 1
    if latest_version:
        new_version_number = latest_version.version_number + 1
    
    note_version = models.NoteVersion(
        note_id=db_note.id,
        title=note.title,
        content=note.content,
        version_number=new_version_number
    )
    db.add(note_version)
    
    db_note.title = note.title
    db_note.content = note.content
    db.commit()
    db.refresh(db_note)
    
    return db_note

@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.query(models.NoteVersion).filter(models.NoteVersion.note_id == note_id).delete()
    db.delete(db_note)
    db.commit()
    
    return None

@router.post("/notes/{note_id}/summarize", response_model=schemas.NoteSummary)
def summarize_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    summary = summarize_text(db_note.content)
    
    return {
        "id": db_note.id,
        "title": db_note.title,
        "summary": summary
    }