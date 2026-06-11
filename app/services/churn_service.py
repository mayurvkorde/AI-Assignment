import logging
logger = logging.getLogger(__name__)

class ChurnService:
    """Service responsible for generating churn predictions using the trained ML model."""

    def __init__(self, model) -> None:
        """Initialize the churn prediction service with a trained model."""
        self.model = model

    def predict_probability(self, features) -> float:
        """Predict and return the customer's churn probability score."""
        logger.debug(
            f"Predicting churn for input shape={features.shape}"
        )
        try:
            result =  self.model.predict_proba(features)[0][1]
            logger.debug(
                f"Predicted churn score={result}"
            )
            return result
        except Exception:
            logger.exception(
                "Churn prediction failed"
            )
            raise