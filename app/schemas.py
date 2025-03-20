from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class NoteUpdate(NoteBase):
    pass

class NoteVersionBase(BaseModel):
    title: str
    content: str
    version_number: int
    created_at: datetime

    class Config:
        from_attributes = True

class Note(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class NoteWithVersions(Note):
    versions: List[NoteVersionBase]

class NoteSummary(BaseModel):
    id: int
    title: str
    summary: str

class AnalyticsResponse(BaseModel):
    total_notes: int
    total_word_count: int
    average_note_length: float
    most_common_words: List[tuple]
    longest_notes: List[tuple]
    shortest_notes: List[tuple]