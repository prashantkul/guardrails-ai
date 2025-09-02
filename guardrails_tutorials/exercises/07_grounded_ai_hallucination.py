"""
TUTORIAL 7: Grounded AI Hallucination Detection Guardrail
==========================================================

OBJECTIVE: Create a guardrail that detects AI hallucinations using grounding techniques.

LEARNING GOALS:
- Understand AI hallucination patterns and detection
- Implement fact-checking against knowledge base
- Use confidence scoring and uncertainty detection
- Create grounding verification mechanisms

DIFFICULTY: ⭐⭐⭐ (Advanced)
"""

import os
import re
from typing import List, Dict, Any, Set, Optional, Tuple
from dotenv import load_dotenv
import requests
from guardrails.errors import ValidationError

load_dotenv()


class GroundedAIHallucinationGuard:
    """
    A guardrail that detects AI hallucinations using grounding and fact-checking.
    
    TODO: Students will implement hallucination detection methods.
    """
    
    def __init__(self, knowledge_base: Dict[str, Any] = None,
                 confidence_threshold: float = 0.7,
                 check_factual_claims: bool = True,
                 check_uncertainty_markers: bool = True,
                 use_llm_verification: bool = True,
                 strict_mode: bool = False):
        """
        Initialize the grounded AI hallucination detection guardrail.
        
        Args:
            knowledge_base: Dictionary of known facts for verification
            confidence_threshold: Minimum confidence required for claims
            check_factual_claims: Whether to verify factual statements
            check_uncertainty_markers: Whether to look for uncertainty language
            use_llm_verification: Whether to use LLM for fact-checking
            strict_mode: If True, be strict about unverified claims
        """
        self.knowledge_base = knowledge_base or {}
        self.confidence_threshold = confidence_threshold
        self.check_factual_claims = check_factual_claims
        self.check_uncertainty_markers = check_uncertainty_markers
        self.use_llm_verification = use_llm_verification
        self.strict_mode = strict_mode
        
        # Patterns that indicate uncertainty or speculation
        self.uncertainty_patterns = [
            r"\bmight\s+be\b", r"\bcould\s+be\b", r"\bmay\s+be\b",
            r"\bpossibly\b", r"\bperhaps\b", r"\bmaybe\b",
            r"\bseems?\s+to\b", r"\bappears?\s+to\b",
            r"\blikely\b", r"\bunlikely\b", r"\bprobably\b",
            r"\bi\s+think\b", r"\bi\s+believe\b", r"\bin\s+my\s+opinion\b",
            r"\bas\s+far\s+as\s+i\s+know\b", r"\bif\s+i\s+recall\b"
        ]
        
        # Patterns that indicate confident factual claims
        self.confident_claim_patterns = [
            r"\bis\s+exactly\b", r"\bis\s+precisely\b", r"\bdefinitely\s+is\b",
            r"\bwithout\s+doubt\b", r"\bcertainly\s+is\b", r"\bobviously\s+is\b",
            r"\bwas\s+born\s+in\b", r"\bdied\s+in\b", r"\bfounded\s+in\b",
            r"\bestablished\s+in\b", r"\binvented\s+in\b",
            r"\baccording\s+to\s+official\b", r"\bdata\s+shows\b"
        ]
        
        # Common hallucination indicators
        self.hallucination_indicators = [
            r"\b\d{4}(?:\s*-\s*\d{4})?\b",  # Years/date ranges (often fabricated)
            r"\b\d+(?:\.\d+)?%\b",  # Specific percentages (often made up)
            r"\$\d+(?:\.\d+)?(?:\s*(?:million|billion|trillion))?\b",  # Monetary amounts
            r"\b\d+(?:\.\d+)?\s*(?:meters?|feet|miles?|kg|pounds?)\b",  # Measurements
        ]
    
    def validate(self, value: str) -> str:
        """
        Validate content for AI hallucinations using grounding techniques.
        
        Args:
            value: Input text to validate
            
        Returns:
            str: Original value if no hallucinations detected
            
        Raises:
            ValidationError: If hallucinations are likely present
        """
        if not value or not isinstance(value, str):
            return value
        
        issues = []
        
        # TODO: STUDENT TASK 1
        # Check for factual claims if enabled
        if self.check_factual_claims:
            # TODO: Call self._check_factual_claims(value)
            factual_issues = []  # TODO: Implement this
        
        # TODO: STUDENT TASK 2
        # Check for uncertainty markers
        if self.check_uncertainty_markers:
            # TODO: Call self._analyze_uncertainty_markers(value)
            uncertainty_score, uncertainty_issues = 0.0, []  # TODO: Implement this
        
        # TODO: STUDENT TASK 3
        # Check against knowledge base
        # TODO: Call self._verify_against_knowledge_base(value)
        kb_issues = []  # TODO: Implement this
        
        # TODO: STUDENT TASK 4
        # Use LLM for verification if enabled
        if self.use_llm_verification:
            # TODO: Call self._llm_fact_check(value)
            llm_issues = []  # TODO: Implement this
        
        # TODO: STUDENT TASK 5
        # Check for hallucination indicators
        # TODO: Call self._detect_hallucination_patterns(value)
        pattern_issues = []  # TODO: Implement this
        
        # TODO: Combine all issues and decide if content should be blocked
        all_issues = factual_issues + uncertainty_issues + kb_issues + llm_issues + pattern_issues
        
        if all_issues:
            # TODO: Create comprehensive error message
            pass
        
        return value
    
    def _check_factual_claims(self, text: str) -> List[str]:
        """
        Check for factual claims that need verification.
        
        TODO: STUDENT TASK 6
        # Identify statements that make factual claims
        # Check if they can be verified
        # YOUR CODE HERE:
        """
        issues = []
        
        # TODO: Look for confident factual claim patterns
        for pattern in self.confident_claim_patterns:
            # TODO: Find matches and extract the claims
            # TODO: Determine if claims are verifiable
            pass
        
        # TODO: Look for specific factual statements
        # Examples: dates, names, numbers, locations
        factual_patterns = [
            r"([A-Z][a-z]+\s+[A-Z][a-z]+)\s+was\s+born\s+in\s+(\d{4})",  # Person born in year
            r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+is\s+located\s+in\s+([A-Z][a-z]+)",  # Location
            r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+was\s+founded\s+in\s+(\d{4})",  # Company/org founded
        ]
        
        for pattern in factual_patterns:
            # TODO: Extract factual claims and check if they seem suspicious
            pass
        
        return issues
    
    def _analyze_uncertainty_markers(self, text: str) -> Tuple[float, List[str]]:
        """
        Analyze uncertainty markers in the text.
        
        TODO: STUDENT TASK 7
        # Calculate uncertainty score based on uncertainty language
        # Higher uncertainty might indicate the AI is guessing
        # YOUR CODE HERE:
        """
        uncertainty_count = 0
        total_sentences = len(self._split_sentences(text))
        issues = []
        
        if total_sentences == 0:
            return 1.0, []
        
        # TODO: Count uncertainty markers
        for pattern in self.uncertainty_patterns:
            # TODO: Count matches of uncertainty pattern
            pass
        
        # TODO: Calculate uncertainty score
        uncertainty_score = 0.0  # TODO: Calculate based on uncertainty_count and total_sentences
        
        # TODO: Add issues if uncertainty is too low for complex claims
        # (Low uncertainty + complex factual claims might indicate hallucination)
        
        return uncertainty_score, issues
    
    def _verify_against_knowledge_base(self, text: str) -> List[str]:
        """
        Verify claims against the knowledge base.
        
        TODO: STUDENT TASK 8
        # Check if any claims in the text contradict known facts
        # YOUR CODE HERE:
        """
        issues = []
        
        if not self.knowledge_base:
            return issues
        
        # TODO: Extract key entities and facts from text
        # TODO: Compare against knowledge base
        # TODO: Look for contradictions
        
        # Example: If knowledge base says "Paris is the capital of France"
        # and text says "London is the capital of France", flag as contradiction
        
        for entity, facts in self.knowledge_base.items():
            # TODO: Check if entity is mentioned in text
            # TODO: Verify if mentioned facts match knowledge base
            pass
        
        return issues
    
    def _llm_fact_check(self, text: str) -> List[str]:
        """
        Use LLM to fact-check claims in the text.
        
        TODO: STUDENT TASK 9
        # Use Groq API to verify factual claims
        # YOUR CODE HERE:
        """
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            return []
        
        # TODO: Create prompt for fact-checking
        prompt = f"""
        Please fact-check the following text for accuracy. Identify any claims that seem:
        1. Factually incorrect
        2. Impossible or highly unlikely
        3. Too specific to be reliable (exact numbers, dates without sources)
        4. Contradictory to well-known facts
        
        Text: "{text}"
        
        Respond with:
        - "ACCURATE" if all claims seem factually correct
        - "QUESTIONABLE: [specific issues]" if there are concerns
        - "INACCURATE: [specific problems]" if there are clear errors
        """
        
        try:
            # TODO: Make API call to Groq
            # TODO: Parse response and identify issues
            pass
        except Exception as e:
            # If LLM fails, return no issues
            return []
    
    def _detect_hallucination_patterns(self, text: str) -> List[str]:
        """
        Detect patterns commonly associated with hallucinations.
        
        TODO: STUDENT TASK 10
        # Look for suspicious patterns that might indicate fabricated content
        # YOUR CODE HERE:
        """
        issues = []
        
        # TODO: Check for overly specific unsourced claims
        # Example: "The company was founded exactly on March 15, 1987 at 2:30 PM"
        
        # TODO: Check for inconsistent information within the text
        
        # TODO: Look for hallucination indicator patterns
        for pattern in self.hallucination_indicators:
            # TODO: Find matches and evaluate if they're suspicious
            pass
        
        # TODO: Check for impossible or contradictory statements
        # Example: "The building is 500 stories tall" (impossible)
        
        return issues
    
    def _split_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences for analysis.
        
        TODO: STUDENT TASK 11
        # Split text by sentence boundaries
        # YOUR CODE HERE:
        """
        # TODO: Use regex to split by sentence-ending punctuation
        sentences = []
        return sentences
    
    def _extract_entities(self, text: str) -> List[str]:
        """
        Extract named entities from text.
        
        TODO: STUDENT TASK 12 (ADVANCED)
        # Extract names, places, organizations, etc.
        # YOUR CODE HERE:
        """
        entities = []
        
        # TODO: Simple entity extraction using patterns
        # Look for capitalized words that might be names, places, etc.
        entity_patterns = [
            r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b",  # Proper nouns
        ]
        
        return entities


def create_hallucination_guard(**kwargs) -> GroundedAIHallucinationGuard:
    """Factory function to create a hallucination detection guard."""
    return GroundedAIHallucinationGuard(**kwargs)


# Test scenarios for students to validate their implementation
def test_grounded_ai_hallucination():
    """Test function for students to verify their implementation."""
    
    print("🧪 Testing Grounded AI Hallucination Detection Guardrail")
    print("=" * 60)
    
    # Test case 1: Basic hallucination detection
    basic_guard = create_hallucination_guard(
        confidence_threshold=0.7,
        check_factual_claims=True,
        use_llm_verification=False
    )
    
    test_cases_1 = [
        ("The weather is nice today.", "SHOULD_PASS"),
        ("I think it might rain later.", "SHOULD_PASS"),  # Has uncertainty
        ("Paris is definitely located in Germany.", "SHOULD_FAIL"),  # False claim
        ("The Eiffel Tower is exactly 324.7392 meters tall.", "SHOULD_FAIL"),  # Too specific
        ("According to studies, most people prefer chocolate.", "SHOULD_PASS"),  # Reasonable claim
        ("Einstein was born in 1879.", "SHOULD_PASS"),  # True fact
    ]
    
    print("\n📝 Test 1: Basic Hallucination Detection")
    _run_hallucination_test_cases(basic_guard, test_cases_1)
    
    # Test case 2: Knowledge base verification
    knowledge_base = {
        "Paris": {"country": "France", "type": "city"},
        "Einstein": {"birth_year": "1879", "field": "physics"},
        "Google": {"founded": "1998", "founders": ["Larry Page", "Sergey Brin"]}
    }
    
    kb_guard = create_hallucination_guard(
        knowledge_base=knowledge_base,
        check_factual_claims=True,
        use_llm_verification=False
    )
    
    test_cases_2 = [
        ("Paris is the capital city of France.", "SHOULD_PASS"),
        ("Einstein was a famous physicist.", "SHOULD_PASS"),
        ("Paris is located in Germany.", "SHOULD_FAIL"),  # Contradicts KB
        ("Google was founded in 1995.", "SHOULD_FAIL"),  # Wrong year
        ("The company has many employees.", "SHOULD_PASS"),  # Vague, no conflict
    ]
    
    print("\n📝 Test 2: Knowledge Base Verification")
    _run_hallucination_test_cases(kb_guard, test_cases_2)
    
    # Test case 3: Uncertainty analysis
    uncertainty_guard = create_hallucination_guard(
        check_uncertainty_markers=True,
        confidence_threshold=0.5,
        strict_mode=True,
        use_llm_verification=False
    )
    
    test_cases_3 = [
        ("I believe this approach might work well.", "SHOULD_PASS"),  # Has uncertainty
        ("This method is definitely the best solution ever created.", "SHOULD_FAIL"),  # Too confident
        ("Perhaps we should consider this option.", "SHOULD_PASS"),  # Uncertain language
        ("The result is exactly 47.3829% accurate.", "SHOULD_FAIL"),  # Too specific, no uncertainty
        ("Studies suggest this could be effective.", "SHOULD_PASS"),  # Appropriate hedging
    ]
    
    print("\n📝 Test 3: Uncertainty Analysis")
    _run_hallucination_test_cases(uncertainty_guard, test_cases_3)


def _run_hallucination_test_cases(guard: GroundedAIHallucinationGuard, test_cases: List[tuple]):
    """Helper function to run hallucination test cases."""
    for i, (text, expected) in enumerate(test_cases, 1):
        try:
            result = guard.validate(text)
            status = "✅ PASSED" if expected == "SHOULD_PASS" else "❌ UNEXPECTED PASS"
            print(f"{i}. '{text[:60]}...' → {status}")
        except ValidationError as e:
            status = "✅ BLOCKED" if expected == "SHOULD_FAIL" else "❌ UNEXPECTED BLOCK"
            print(f"{i}. '{text[:60]}...' → {status}")
            if expected == "SHOULD_FAIL":
                print(f"   Reason: {e}")


if __name__ == "__main__":
    """
    STUDENT INSTRUCTIONS:
    ====================
    
    1. Complete the TODO sections in the GroundedAIHallucinationGuard class
    2. Start with basic claim detection (Tasks 1, 6)
    3. Implement uncertainty analysis (Tasks 2, 7)
    4. Add knowledge base verification (Tasks 3, 8)
    5. Optionally implement LLM verification (Tasks 4, 9)
    6. Add pattern-based detection (Tasks 5, 10)
    7. Complete helper methods (Tasks 11-12)
    8. Run this file to test: python 07_grounded_ai_hallucination.py
    9. All tests should pass with appropriate PASS/BLOCK results
    
    HINTS:
    ------
    - For uncertainty detection: count uncertainty words vs confident claims
    - For factual claims: look for specific dates, numbers, proper nouns
    - For knowledge base: compare extracted facts against known information
    - For patterns: detect overly specific unsourced claims
    - For LLM verification: ask the model to fact-check specific claims
    
    HALLUCINATION TYPES:
    -------------------
    1. Factual errors: Wrong dates, names, locations
    2. Fabricated details: Made-up specific numbers, quotes
    3. Impossible claims: Physically/logically impossible statements
    4. Inconsistencies: Contradictory information within text
    5. Overconfidence: Too certain about uncertain information
    
    GROUNDING TECHNIQUES:
    --------------------
    - Knowledge base lookup: Verify against known facts
    - Uncertainty quantification: Measure confidence levels  
    - Source attribution: Check for proper citations
    - Consistency checking: Look for internal contradictions
    - Plausibility assessment: Evaluate if claims are reasonable
    
    EXTENSION CHALLENGES:
    --------------------
    - Add real-time fact-checking APIs (Wikipedia, fact-check services)
    - Implement semantic similarity for claim matching
    - Add temporal consistency checking (timeline validation)
    - Create domain-specific knowledge bases
    - Implement confidence calibration and uncertainty quantification
    """
    test_grounded_ai_hallucination()