from fastapi import Request, HTTPException
from pandas import DataFrame
from app.orchestrations.retention_orchestration_layer import retention_graph
from app.schema.retention import RetentionResponse
from typing import Dict
from app.config.constant import HEALTHY_STATUS, REVIEW_REQUIRED_STATUS, READY_TO_SEND_STATUS
import logging


logger = logging.getLogger(__name__)

async def get_retention(
    request: Request,
    customer_id: str,
    customer_data: DataFrame
) -> RetentionResponse:
    """Execute the customer retention workflow and return the final retention response."""
    logger.info(f"Starting retention workflow for customer_id={customer_id}")

    churn_service = request.app.state.churn_service
    llm_service = request.app.state.llm_service

    customer_data = customer_data.drop(columns=["customerID"])

    # Ensure single row
    customer_data = customer_data.iloc[[0]]

    retention_state = {
        "customer": customer_data.to_dict(orient="records")[0],
        "customer_dataframe": customer_data,
        "services": {
            "churn": churn_service,
            "llm": llm_service,
        }
    }
    logger.info(
        f"Invoking retention graph for customer_id={customer_id}"
    )
    try:
        result = await retention_graph.ainvoke(retention_state)
    except Exception as ex:
        logger.exception(
            f"Retention workflow failed for customer_id={customer_id}"
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to execute retention workflow."
        )

    logger.info(
        f"Graph execution completed for customer_id={customer_id}"
    )
    # Low-risk customer
    if result.get("risk") == "low":
        logger.info(
            f"Customer classified as HEALTHY customer_id={customer_id} score={result.get('score')}"
        )
        return RetentionResponse(
            customer_id=customer_id,
            status=HEALTHY_STATUS,
            churn_score=round(result.get("score", 0), 4)
        )

    return response_validation(result,customer_id)

def response_validation(result: Dict, customer_id: str) -> RetentionResponse:
    """Predict the customer's churn probability using the trained ML model."""
    validation = result.get("validation", {})

    validation_score = validation.get("score", 0)

    # Human review required
    if validation_score < 80:
        logger.warning(
            f"Email validation failed for customer_id={customer_id} score={validation_score}"
        )
        return RetentionResponse(
            customer_id=customer_id,
            status=REVIEW_REQUIRED_STATUS,
            churn_score=round(result.get("score", 0), 4),
            validation_score=validation_score,
            violations=validation.get("violations", []),
            generated_email=result.get("email")
        )

    # Ready to send
    logger.info(
        f"Retention email approved for customer_id={customer_id}"
    )
    return RetentionResponse(
        customer_id=customer_id,
        status=READY_TO_SEND_STATUS,
        churn_score=round(result.get("score", 0), 4),
        validation_score=validation_score,
        retention_email=result.get("email")
    )


