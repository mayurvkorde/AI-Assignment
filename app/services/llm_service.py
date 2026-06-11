import json
from openai import AsyncOpenAI, OpenAI
from typing import Dict
import logging
from app.utils.json_parser import safe_json_parse

logger = logging.getLogger(__name__)


class LLMService:
    """Service responsible for generating and validating retention communications using an LLM."""
    def __init__(self, api_key: str, model: str):
        """Initialize the LLM client with the configured model and API credentials."""
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def generate_email(
        self,
        context: Dict,
        brand_guidelines: str
    ) -> Dict:
        """Generate a personalized retention email based on customer context and brand guidelines."""
        system_prompt = brand_guidelines

        user_prompt = f"""
            Generate a retention email for the following customer.
            
            Customer Details:
            {json.dumps(context, indent=2)}
            
            Requirements:
            1. Thank the customer for being with Vodafone.
            2. Reference their current services.
            3. Reinforce the value they receive.
            4. Encourage them to continue their relationship with Vodafone.
            5. Keep the email under 200 words.
            
            Return ONLY valid JSON:

            {{
                "subject": "string",
                "email_body": "string"
            }}
        """
        logger.info(
            f"Calling LLM model={self.model} for email generation"
        )
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    },
                ],
                temperature=0.3,
                response_format={"type": "json_object"},
            )
        except Exception:
            logger.exception("Email generation failed")
            raise
        logger.info(
            "LLM email generation completed"
        )
        content = response.choices[0].message.content
        return safe_json_parse(content)

    async def validate_email(
        self,
        email: dict,
        context: dict,
        review_rules: str
    ) -> Dict:
        """Validate the generated retention email against predefined review and compliance rules."""
        system_prompt = review_rules

        user_prompt = f"""
            Customer Context:
            {json.dumps(context, indent=2)}
    
            Generated Email:
            {json.dumps(email, indent=2)}
    
            Review the email and return JSON:
    
            {{
                "score": 0,
                "passed": false,
                "human_review_required": true,
                "violations": []
            }}
        """
        logger.info(
            f"Calling LLM model={self.model} for email validation"
        )
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                temperature=0
            )
        except Exception:
            logger.exception("Email validation failed")
            raise
        logger.info(
            f"Calling LLM model={self.model} for email validation"
        )
        content = response.choices[0].message.content

        return safe_json_parse(content)