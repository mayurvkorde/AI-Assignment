from typing import Dict, Any, List, Optional, TypedDict
from pydantic import BaseModel

class RetentionResponse(BaseModel):
    customer_id: str
    status: str
    churn_score: float
    validation_score: Optional[float] = None
    retention_email: Optional[Dict] = None
    violations: Optional[List] = None
    generated_email: Optional[str] = None


class RetentionState(TypedDict):
    customer: Dict[str, Any]
    customer_dataframe: Any
    services: Dict[str, Any]
    score: float
    risk: str
    context: Dict[str, Any]
    email: Dict[str, Any]
    validation: Dict[str, Any]
