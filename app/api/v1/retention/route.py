from fastapi import APIRouter, Depends
import logging
from app.api.utils.utils import verify_api_key
from fastapi import HTTPException, Request
from app.api.v1.retention.controller import get_retention
from app.schema.retention import RetentionResponse

logger = logging.getLogger(__name__)


retention_router = APIRouter(
    prefix="/retention",
    tags=["retention"]
)


@retention_router.get(
    "/{customer_id}",
    response_model=RetentionResponse,
    response_description="Returns customer retention analysis including churn score, risk status, validation outcome, and retention email when applicable.",
    response_model_exclude_none=True
)
async def get_retention_data(
    customer_id: str,
    request: Request,
    auth=Depends(verify_api_key)
) -> RetentionResponse:
    """Retrieve customer information and initiate the retention workflow."""
    try:
        logger.info(f"Received retention request for customer_id={customer_id}")

        customer_dataset = request.app.state.customer_data
        customer_data = customer_dataset[customer_dataset["customerID"] == customer_id]

        if customer_data.empty:
            logger.warning(f"Customer not found for customer_id={customer_id}")

            raise HTTPException(
                status_code=404,
                detail=f"Customer data not found: {customer_id}"
            )
        logger.info(f"Customer data found for customer_id={customer_id}")

        result = await get_retention(
            request=request,
            customer_id=customer_id,
            customer_data=customer_data,
        )
        return result
    except Exception:
        logger.exception(
            f"Retention request failed for customer_id={customer_id}"
        )
        raise



