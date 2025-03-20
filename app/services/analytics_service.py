from sqlalchemy.orm import Session
from app import models
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

nltk.download('punkt_tab')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def generate_analytics(db: Session):
    """
    Generate analytics data for all notes in the database.
    """
    notes = db.query(models.Note).all()
    
    if not notes:
        return {
            "total_notes": 0,
            "total_word_count": 0,
            "average_note_length": 0,
            "most_common_words": [],
            "longest_notes": [],
            "shortest_notes": []
        }
    
    all_words = []
    note_lengths = []
    
    for note in notes:
        words = word_tokenize(note.content.lower())
        words = [word for word in words if word.isalnum()]
        all_words.extend(words)
        note_lengths.append((note.id, note.title, len(words)))
    
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in all_words if word not in stop_words]

    total_notes = len(notes)
    total_word_count = len(all_words)
    average_note_length = total_word_count / total_notes if total_notes > 0 else 0

    word_counts = Counter(filtered_words)
    most_common_words = word_counts.most_common(10)

    sorted_notes = sorted(note_lengths, key=lambda x: x[2])
    shortest_notes = sorted_notes[:3] if len(sorted_notes) >= 3 else sorted_notes
    longest_notes = sorted_notes[-3:][::-1] if len(sorted_notes) >= 3 else sorted_notes[::-1]
    
    return {
        "total_notes": total_notes,
        "total_word_count": total_word_count,
        "average_note_length": average_note_length,
        "most_common_words": most_common_words,
        "longest_notes": longest_notes,
        "shortest_notes": shortest_notes
    }