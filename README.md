# AI-Enhanced Notes Management System

## Project Overview

This project is a RESTful API for managing notes with advanced capabilities, including automatic versioning, AI-powered summarization, and text analytics. The system is built using FastAPI and provides a comprehensive solution for note management with intelligent features.

## Features

* **CRUD Operations** : Create, read, update, and delete notes
* **Automatic Versioning** : Track all changes to notes with complete version history
* **AI Summarization** : Generate concise summaries of notes using Google Gemini AI
* **Text Analytics** : Gather insights about your notes collection, including:
* Statistical analysis (total notes, word count, average length)
* Most common words analysis
* Identification of longest and shortest notes

## Tech Stack

* **FastAPI** : High-performance web framework
* **SQLAlchemy** : ORM for database interactions
* **SQLite** : Lightweight database storage
* **Google Gemini API** : AI model for text summarization
* **NLTK** : Natural language processing for analytics
* **Pydantic** : Data validation and serialization

## Project Structure


```
app/├── database.py      # Database configuration
├── main.py          # Application entry point
├── models.py        # SQLAlchemy data models
├── schemas.py       # Pydantic schemas
├── routers/         # API endpoints
│   ├── notes.py     # Notes endpoints
│   └── analytics.py # Analytics endpoints
└── services/        # Business logic**  
├── ai_service.py       # Gemini API **integration**  
└── analytics_service.py # Text analytics **logictests/               # Unit tests
```


## Installation and Setup

1. **Clone the repository**
2. **Set up a virtual environment**

   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```
3. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```
4. **Configure environment variables** Create a [.env](vscode-file://vscode-app/c:/Users/koval/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) file with your Google Gemini API key:

   ```
   GEMINI_API_KEY=your_api_key
   ```
5. **Run the application**

   ```
   uvicorn app.main:app --reload
   ```

## API Documentation

Once running, API documentation is available at `http://localhost:8000/docs`

### Key Endpoints

#### Notes

* `POST /api/notes/` - Create a new note
* `GET /api/notes/` - Get all notes
* `GET /api/notes/{note_id}` - Get a specific note
* `PUT /api/notes/{note_id}` - Update a note
* `DELETE /api/notes/{note_id}` - Delete a note
* `POST /api/notes/{note_id}/summarize` - Generate AI summary for a note
* `GET /api/notes/{note_id}/versions` - Get all versions of a note

#### Analytics

* `GET /api/analytics/` - Get analytics data for all notes

## Implementation Details

### Note Versioning

Each note modification automatically generates a new version record, allowing for complete history tracking. Versions are numbered sequentially and include timestamps.

### AI Integration

The system uses Google's Gemini API to generate intelligent summaries of note content. If the API is unavailable, a fallback mechanism provides sample summarization.

### Text Analytics

The analytics service uses NLTK to process note content, excluding common stop words to provide meaningful insights about the text collection.

## Testing

Run the test suite with:

```
pytest
```

The tests cover core functionality including:

* Note creation
* Note retrieval
* Version tracking during updates
* Note deletion
