from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.ai import (
    AIQueryRequest,
    AIQueryResponse,
)
from app.services.ai_service import (
    process_ai_query,
)


router = APIRouter(
    prefix="/ai",
    tags=["AI Assistant"],
)


@router.post(
    "/query",
    response_model=AIQueryResponse,
)
def ai_query_endpoint(
    query_data: AIQueryRequest,
    db: Session = Depends(get_db),
):
    return process_ai_query(
        db=db,
        query=query_data.query,
    )