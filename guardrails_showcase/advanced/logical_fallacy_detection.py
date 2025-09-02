import os
import re
from typing import List, Dict, Any
from dotenv import load_dotenv
import requests
from guardrails.errors import ValidationError

load_dotenv()


def logical_fallacy_validator(value: str, use_llm: bool = True, 
                             require_structure: bool = False) -> str:
    """Validator function that detects logical fallacies"""
    
    # Pattern-based detection for common logical fallacies
    fallacy_patterns = {
        "ad_hominem": [
            r"\b(you are|you're) (stupid|dumb|ignorant|crazy|wrong)\b",
            r"\bonly (idiots|fools) (believe|think|say)\b",
            r"\b(he|she|they) (can't be trusted|is lying|is biased)\b"
        ],
        "straw_man": [
            r"\bso you're saying\b",
            r"\byou (think|believe) that all\b",
            r"\baccording to your logic\b"
        ],
        "false_dilemma": [
            r"\b(either|if not).+(or|then).+(no other|only two|must choose)\b",
            r"\byou're either (with us or against us|part of|not part of)\b",
            r"\bthere are only two (options|choices|ways)\b"
        ],
        "appeal_to_authority": [
            r"\b(all|most) (experts|scientists|doctors) (say|agree|believe)\b",
            r"\b(famous|well-known) (people|celebrities) (endorse|support)\b",
            r"\bif it's good enough for.+it's good enough\b"
        ],
        "bandwagon": [
            r"\b(everyone|everybody) (is doing|believes|knows)\b",
            r"\bmillions of people can't be wrong\b",
            r"\ball the cool kids\b",
            r"\bdon't be the only one\b"
        ],
        "circular_reasoning": [
            r"\bbecause (it is|that's how|that's what)\b",
            r"\bit's true because.+says so\b",
            r"\bthe bible says.+because.+bible\b"
        ],
        "slippery_slope": [
            r"\bif we (allow|permit|let).+then (eventually|soon|next)\b",
            r"\bthis will lead to\b",
            r"\bonce we start.+where does it end\b",
            r"\bgive them an inch.+take a mile\b"
        ],
        "hasty_generalization": [
            r"\ball (men|women|people|politicians) are\b",
            r"\bevery (single|one of) them\b",
            r"\bthey always\b",
            r"\bnever trust a\b"
        ]
    }
    
    # Detect fallacy patterns using regex
    detected = {}
    text_lower = value.lower()
    
    for fallacy, patterns in fallacy_patterns.items():
        matches = []
        for pattern in patterns:
            found = re.findall(pattern, text_lower, re.IGNORECASE)
            if found:
                matches.extend([str(match) for match in found])
        if matches:
            detected[fallacy] = matches
    
    # Calculate fallacy score
    fallacy_score = 0
    detected_fallacies = []
    
    # Score based on pattern matches
    for fallacy, matches in detected.items():
        fallacy_score += len(matches) * 2
        detected_fallacies.extend([f"{fallacy.replace('_', ' ')}: {match}" for match in matches])
    
    # Additional checks for specific fallacy indicators
    # Check for excessive emotional language
    emotional_words = ['outrageous', 'ridiculous', 'absurd', 'insane', 'crazy', 'stupid']
    emotional_count = sum(1 for word in emotional_words if word in text_lower)
    if emotional_count >= 2:
        fallacy_score += 1
        detected_fallacies.append("appeal to emotion: excessive emotional language")
    
    # Check for absolute statements
    absolute_words = ['always', 'never', 'all', 'none', 'every', 'completely', 'totally']
    absolute_count = sum(1 for word in absolute_words if f' {word} ' in f' {text_lower} ')
    if absolute_count >= 2:
        fallacy_score += 1
        detected_fallacies.append("hasty generalization: absolute statements")
    
    # Check argument structure if required
    if require_structure:
        structure_issues = _check_argument_structure(value)
        if structure_issues:
            fallacy_score += len(structure_issues)
            detected_fallacies.extend([f"structure: {issue}" for issue in structure_issues])
    
    # LLM-based analysis (optional, if Groq API key is available)
    if use_llm and os.getenv("GROQ_API_KEY"):
        try:
            llm_score = _llm_fallacy_analysis(value)
            fallacy_score += llm_score
        except Exception:
            pass  # Continue without LLM if there's an error
    
    # If high fallacy score, block the content
    if fallacy_score >= 3 or len(detected_fallacies) >= 2:
        raise ValidationError(
            f"Content contains logical fallacies: {detected_fallacies}. "
            "Please revise to use sound logical reasoning."
        )
    
    return value


def _check_argument_structure(text: str) -> List[str]:
    """Check for proper argument structure"""
    text_lower = text.lower()
    issues = []
    
    # Indicators of logical structure
    premise_indicators = [
        'because', 'since', 'given that', 'as', 'for', 'due to',
        'owing to', 'seeing that', 'in view of', 'considering'
    ]
    
    conclusion_indicators = [
        'therefore', 'thus', 'hence', 'so', 'consequently',
        'it follows that', 'we can conclude', 'this means',
        'as a result', 'accordingly'
    ]
    
    evidence_indicators = [
        'studies show', 'research indicates', 'data suggests',
        'according to', 'statistics reveal', 'evidence shows',
        'for example', 'specifically', 'in particular'
    ]
    
    # Check for premise indicators
    has_premises = any(indicator in text_lower for indicator in premise_indicators)
    
    # Check for conclusion indicators
    has_conclusions = any(indicator in text_lower for indicator in conclusion_indicators)
    
    # Check for evidence
    has_evidence = any(indicator in text_lower for indicator in evidence_indicators)
    
    # Validate argument structure
    if not has_premises:
        issues.append("lacks clear premise indicators")
    
    if not has_conclusions:
        issues.append("lacks clear conclusion indicators")
    
    if not has_evidence:
        issues.append("lacks supporting evidence")
    
    # Check for proper argument length (avoid one-liners)
    sentences = re.split(r'[.!?]+', text.strip())
    if len([s for s in sentences if s.strip()]) < 2:
        issues.append("too brief for proper argumentation")
    
    return issues


def _llm_fallacy_analysis(text: str) -> int:
    """Use Groq LLM for advanced fallacy detection"""
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        return 0
    
    groq_url = "https://api.groq.com/openai/v1/chat/completions"
    
    prompt = f"""
    Analyze the following text for logical fallacies. Look for these common fallacies:
    1. Ad Hominem - attacking the person instead of the argument
    2. Straw Man - misrepresenting someone's argument
    3. False Dilemma - presenting only two options when more exist
    4. Appeal to Authority - claiming something is true because an authority says so
    5. Bandwagon - claiming something is true because many people believe it
    6. Circular Reasoning - using the conclusion as evidence
    7. Slippery Slope - claiming one event will lead to negative events
    8. Hasty Generalization - drawing broad conclusions from limited examples
    9. Appeal to Emotion - manipulating emotions instead of using logic
    10. Red Herring - introducing irrelevant information
    
    Text: "{text}"
    
    Respond with only a number from 0-3 representing fallacy level:
    0 = No fallacies detected
    1 = Minor fallacies
    2 = Moderate fallacies
    3 = Severe fallacies
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


class FallacyGuard:
    """Simple guardrail for logical fallacy detection"""
    
    def __init__(self, detector_type: str = "fallacy", use_llm: bool = True, **kwargs):
        self.detector_type = detector_type
        self.use_llm = use_llm
        self.kwargs = kwargs
        
        # Validate detector type
        valid_types = ['fallacy', 'structure']
        if detector_type not in valid_types:
            raise ValueError(f"Unknown detector type: {detector_type}")
    
    def validate(self, value: str) -> str:
        """Validate the input text"""
        if self.detector_type == "fallacy":
            return logical_fallacy_validator(value, use_llm=self.use_llm)
        elif self.detector_type == "structure":
            return logical_fallacy_validator(value, use_llm=self.use_llm, require_structure=True)
        else:
            raise ValueError(f"Unknown detector type: {self.detector_type}")


def create_fallacy_guard(detector_type: str = "fallacy", use_llm: bool = True, **kwargs) -> FallacyGuard:
    """Create a logical fallacy detection guardrail"""
    return FallacyGuard(detector_type, use_llm, **kwargs)


def demo_fallacy_detection():
    """Demo function to test logical fallacy detection"""
    
    # Test fallacy detection
    guard_fallacy = create_fallacy_guard("fallacy", use_llm=True)
    
    test_inputs = [
        "Based on research, our approach shows significant improvement in efficiency metrics.",
        "You're stupid if you don't agree with this obviously correct solution.",
        "Either you support our proposal completely or you're against progress entirely.",
        "All experts agree that this is the only viable solution to the problem.",
        "Everyone is using this technology, so it must be the right choice.",
        "This is true because it's always been true and that's how things work.",
        "If we allow this change, eventually everything will collapse and chaos will ensue."
    ]
    
    results_fallacy = []
    for text in test_inputs:
        try:
            validated = guard_fallacy.validate(text)
            results_fallacy.append({"input": text, "status": "PASSED", "output": validated})
        except Exception as e:
            results_fallacy.append({"input": text, "status": "BLOCKED", "reason": str(e)})
    
    # Test argument structure validation
    guard_structure = create_fallacy_guard("structure", use_llm=False)
    
    test_arguments = [
        "Because studies show improved performance, and given that user feedback is positive, therefore we should implement this solution.",
        "This is good.",
        "Since our analysis indicates cost savings, we can conclude this approach is beneficial.",
        "The solution works well and users like it, so we should use it.",
        "According to research data, performance improves by 30%. Therefore, this method is recommended."
    ]
    
    results_structure = []
    for text in test_arguments:
        try:
            validated = guard_structure.validate(text)
            results_structure.append({"input": text, "status": "PASSED", "output": validated})
        except Exception as e:
            results_structure.append({"input": text, "status": "BLOCKED", "reason": str(e)})
    
    return {
        "fallacy_detection": results_fallacy,
        "argument_structure": results_structure
    }