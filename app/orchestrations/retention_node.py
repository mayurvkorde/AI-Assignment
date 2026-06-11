from app.schema.retention import RetentionState
import logging

logger = logging.getLogger(__name__)


def ml_node(retention_state: RetentionState) -> RetentionState:
    """Predict the churn probability and update the workflow state with the prediction score."""
    logger.info("Executing churn prediction")

    churn_service = retention_state["services"]["churn"]

    retention_state["score"] = churn_service.predict_probability(
        retention_state["customer_dataframe"]
    )
    logger.info(
        f"Churn score calculated: {retention_state['score']:.4f}"
    )
    return retention_state

def risk_node(retention_state: RetentionState) -> RetentionState:
    """Determine the customer's retention risk category based on the churn score."""

    retention_state["risk"] = "high" if retention_state["score"] >= 0.5 else "low"
    logger.info(
        f"Risk classification completed: {retention_state['risk']}"
    )
    return retention_state


def context_node(retention_state: RetentionState) -> RetentionState:
    """Build a customer context object containing attributes relevant for retention messaging."""

    customer_context = retention_state["customer"]

    retention_state["context"] = {
        "tenure": customer_context.get("tenure"),
        "contract": customer_context.get("Contract"),
        "internet_service": customer_context.get("InternetService"),
        "phone_service": customer_context.get("PhoneService"),
        "multiple_lines": customer_context.get("MultipleLines"),
        "online_security": customer_context.get("OnlineSecurity"),
        "online_backup": customer_context.get("OnlineBackup"),
        "device_protection": customer_context.get("DeviceProtection"),
        "tech_support": customer_context.get("TechSupport"),
        "streaming_tv": customer_context.get("StreamingTV"),
        "streaming_movies": customer_context.get("StreamingMovies"),
        "monthly_charges": customer_context.get("MonthlyCharges")
    }

    return retention_state


async def llm_node(retention_state: RetentionState) -> RetentionState:
    """Generate a personalized retention email using customer context and brand guidelines."""

    llm_service = retention_state["services"]["llm"]

    with open(
        "app/prompts/vodafone_brand_guidelines.md",
        encoding="utf-8"
    ) as f:
        brand_guidelines = f.read()
    logger.info(
        "Generating personalized retention email"
    )
    retention_state["email"] = (
        await llm_service.generate_email(
            context=retention_state["context"],
            brand_guidelines=brand_guidelines
        )
    )
    logger.info(
        "Retention email generated successfully"
    )
    return retention_state

async def validation_node(retention_state: RetentionState) -> RetentionState:
    """Validate the generated retention email and record validation results in the workflow state."""

    llm_service = retention_state["services"]["llm"]
    with open(
        "app/prompts/vodafone_email_review_rules.md",
        encoding="utf-8"
    ) as f:
        review_rules = f.read()
    logger.info(
        "Validating generated retention email"
    )
    validation_result = (
        await llm_service.validate_email(
            email=retention_state["email"],
            context=retention_state["context"],
            review_rules=review_rules
        )
    )
    logger.info(
        f"Validation completed with score={validation_result.get('score')}"
    )
    retention_state["validation"] = validation_result
    return retention_state