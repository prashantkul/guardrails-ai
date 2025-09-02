import re
from typing import List, Dict, Any
from guardrails.errors import ValidationError


def competitor_mention_validator(value: str, competitors: List[str], case_sensitive: bool = False) -> str:
    """Validator function that blocks competitor mentions"""
    if not case_sensitive:
        value_lower = value.lower()
        competitors_lower = [comp.lower() for comp in competitors]
    else:
        value_lower = value
        competitors_lower = competitors
        
    for competitor in competitors_lower:
        pattern = r'\b' + re.escape(competitor) + r'\b'
        if re.search(pattern, value_lower):
            raise ValidationError(
                f"Content mentions competitor: {competitor}. "
                "Please revise to focus on our own solutions."
            )
    return value


class CompetitorGuard:
    """Simple guardrail that blocks competitor mentions"""
    
    def __init__(self, competitors: List[str], case_sensitive: bool = False):
        self.competitors = competitors
        self.case_sensitive = case_sensitive
    
    def validate(self, value: str) -> str:
        """Validate the input text"""
        return competitor_mention_validator(value, self.competitors, self.case_sensitive)


def create_competitor_guard(competitors: List[str]) -> CompetitorGuard:
    """Create a guardrail that blocks competitor mentions"""
    return CompetitorGuard(competitors)


# Example usage
TECH_COMPETITORS = [
    "OpenAI",
    "Google", 
    "Microsoft",
    "Amazon",
    "Meta",
    "Anthropic",
    "Cohere",
    "Hugging Face"
]

def demo_competitor_blocking():
    guard = create_competitor_guard(TECH_COMPETITORS)
    
    test_inputs = [
        "Our AI solution is great for customer service.",
        "Unlike OpenAI's GPT, our model is more accurate.",
        "We provide better results than Google's offerings.", 
        "This is a revolutionary approach to AI development."
    ]
    
    results = []
    for text in test_inputs:
        try:
            validated = guard.validate(text)
            results.append({"input": text, "status": "PASSED", "output": validated})
        except Exception as e:
            results.append({"input": text, "status": "BLOCKED", "reason": str(e)})
    
    return results