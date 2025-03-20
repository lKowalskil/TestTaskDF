from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..services.analytics_service import generate_analytics

router = APIRouter()

@router.get("/analytics/", response_model=schemas.AnalyticsResponse)
def get_analytics(db: Session = Depends(get_db)):
    analytics_data = generate_analytics(db)
    return analytics_data