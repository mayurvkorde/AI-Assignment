import json
import re


def safe_json_parse(content: str) -> dict:
    """Extract and parse JSON safely from LLM output."""

    content = re.sub(r"```json|```", "", content).strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        start = content.find("{")
        end = content.rfind("}") + 1

        if start != -1 and end != -1:
            return json.loads(content[start:end])

        raise