import os
import re
from typing import List, Dict, Any
from dotenv import load_dotenv
import requests
from guardrails.errors import ValidationError

load_dotenv()


def psychological_manipulation_validator(value: str, use_llm: bool = True) -> str:
    """Validator function that detects psychological manipulation techniques"""
    
    # Pattern-based detection for common manipulation tactics
    manipulation_patterns = {
        "urgency": [
            r"\b(urgent|immediately|now|hurry|limited time|expires soon|act fast)\b",
            r"\b(don't wait|last chance|only \d+ left|while supplies last)\b"
        ],
        "fear_appeal": [
            r"\b(dangerous|risky|unsafe|threat|warning|alert|beware)\b",
            r"\b(you'll regret|miss out|lose forever|never again)\b"
        ],
        "social_proof": [
            r"\b(everyone is|most people|thousands of|millions of)\b",
            r"\b(join the crowd|be like others|don't be left behind)\b"
        ],
        "authority": [
            r"\b(experts say|doctors recommend|studies show|proven by)\b",
            r"\b(as seen on|endorsed by|approved by|certified)\b"
        ],
        "scarcity": [
            r"\b(limited|exclusive|rare|only \d+|few remaining)\b",
            r"\b(sold out soon|running out|almost gone)\b"
        ]
    }
    
    # Detect manipulation patterns using regex
    detected = {}
    text_lower = value.lower()
    
    for category, patterns in manipulation_patterns.items():
        matches = []
        for pattern in patterns:
            found = re.findall(pattern, text_lower, re.IGNORECASE)
            matches.extend(found)
        if matches:
            detected[category] = matches
    
    # Calculate manipulation score
    manipulation_score = 0
    detected_techniques = []
    
    # Score based on pattern matches
    for category, matches in detected.items():
        manipulation_score += len(matches) * 1
        detected_techniques.extend([f"{category}: {match}" for match in matches])
    
    # Additional checks for specific indicators
    # Check for excessive emotional language
    emotional_words = ['outrageous', 'ridiculous', 'absurd', 'insane', 'crazy', 'stupid']
    emotional_count = sum(1 for word in emotional_words if word in text_lower)
    if emotional_count >= 2:
        manipulation_score += 1
        detected_techniques.append("appeal to emotion: excessive emotional language")
    
    # Check for absolute statements
    absolute_words = ['always', 'never', 'all', 'none', 'every', 'completely', 'totally']
    absolute_count = sum(1 for word in absolute_words if f' {word} ' in f' {text_lower} ')
    if absolute_count >= 2:
        manipulation_score += 1
        detected_techniques.append("hasty generalization: absolute statements")
    
    # LLM-based analysis (optional, if Groq API key is available)
    if use_llm and os.getenv("GROQ_API_KEY"):
        try:
            llm_score = _llm_manipulation_analysis(value)
            manipulation_score += llm_score
        except Exception:
            pass  # Continue without LLM if there's an error
    
    # If high manipulation score or specific patterns detected, block
    if manipulation_score >= 3 or len(detected_techniques) >= 2:
        raise ValidationError(
            f"Content contains psychological manipulation techniques: {detected_techniques}. "
            "Please revise to use ethical persuasion methods."
        )
    
    return value


def _llm_manipulation_analysis(text: str) -> int:
    """Use Groq LLM for advanced manipulation detection"""
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        return 0
    
    groq_url = "https://api.groq.com/openai/v1/chat/completions"
    
    prompt = f"""
    Analyze the following text for psychological manipulation techniques. 
    Look for:
    1. Emotional manipulation (fear, guilt, shame)
    2. Cognitive biases exploitation (anchoring, confirmation bias)
    3. Persuasion techniques (reciprocity, commitment, liking)
    4. Deceptive practices (misleading claims, false urgency)
    
    Text: "{text}"
    
    Respond with only a number from 0-3 representing manipulation level:
    0 = No manipulation detected
    1 = Mild manipulation
    2 = Moderate manipulation  
    3 = High manipulation
    """
    
    try:
        response = requests.post(
            groq_url,
            headers={
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mixtral-8x7b-32768",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,
                "max_tokens": 10
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            llm_response = result["choices"][0]["message"]["content"].strip()
            # Extract number from response
            try:
                return int(llm_response)
            except:
                return 0
        else:
            return 0
            
    except Exception:
        return 0


class ManipulationGuard:
    """Simple guardrail for psychological manipulation detection"""
    
    def __init__(self, use_llm: bool = True):
        self.use_llm = use_llm
    
    def validate(self, value: str) -> str:
        """Validate the input text"""
        return psychological_manipulation_validator(value, self.use_llm)


def create_manipulation_guard(use_llm: bool = True) -> ManipulationGuard:
    """Create a guardrail that detects psychological manipulation"""
    return ManipulationGuard(use_llm)


def demo_manipulation_detection():
    """Demo function to test manipulation detection"""
    guard = create_manipulation_guard(use_llm=True)
    
    test_inputs = [
        "Our product is great and can help improve your productivity.",
        "ACT NOW! Limited time offer - only 3 left! Don't miss out or you'll regret it forever!",
        "Experts say this is dangerous - you need our protection immediately!",
        "Everyone is buying this - don't be left behind! Join thousands of satisfied customers.",
        "This exclusive offer expires in 1 hour. Most people who wait lose this opportunity forever."
    ]
    
    results = []
    for text in test_inputs:
        try:
            validated = guard.validate(text)
            results.append({"input": text, "status": "PASSED", "output": validated})
        except Exception as e:
            results.append({"input": text, "status": "BLOCKED", "reason": str(e)})
    
    return results