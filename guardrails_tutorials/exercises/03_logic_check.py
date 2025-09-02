"""
TUTORIAL 3: Logic Check Guardrail
==================================

OBJECTIVE: Create a guardrail that validates logical consistency in AI responses.

LEARNING GOALS:
- Implement basic logical consistency checks
- Detect contradictions in statements
- Validate mathematical calculations
- Check cause-and-effect relationships

DIFFICULTY: ⭐⭐⭐ (Advanced)
"""

import re
import math
from typing import List, Dict, Any, Tuple, Optional
from guardrails.errors import ValidationError


class LogicCheckGuard:
    """
    A guardrail that performs logical consistency checks on content.
    
    TODO: Students will implement various logical validation methods.
    """
    
    def __init__(self, check_contradictions: bool = True, check_math: bool = True,
                 check_causality: bool = True, strict_mode: bool = False):
        """
        Initialize the logic check guardrail.
        
        Args:
            check_contradictions: Whether to check for logical contradictions
            check_math: Whether to validate mathematical statements
            check_causality: Whether to check cause-and-effect consistency
            strict_mode: If True, be strict about logical requirements
        """
        self.check_contradictions = check_contradictions
        self.check_math = check_math
        self.check_causality = check_causality
        self.strict_mode = strict_mode
        
        # Predefined contradiction patterns
        self.contradiction_patterns = [
            (r'\b(always|never)\b.*\b(sometimes|occasionally)\b', "Absolute vs. conditional statements"),
            (r'\b(all|every)\b.*\b(some|few|many)\b.*\b(not|n\'t)\b', "Universal vs. particular statements"),
            (r'\b(impossible|can\'t)\b.*\b(possible|can|could)\b', "Possibility contradictions"),
            (r'\b(increase|rise|grow)\b.*\b(decrease|fall|shrink)\b', "Directional contradictions"),
        ]
    
    def validate(self, value: str) -> str:
        """
        Validate logical consistency of the content.
        
        Args:
            value: Input text to validate
            
        Returns:
            str: Original value if logically consistent
            
        Raises:
            ValidationError: If logical inconsistencies are found
        """
        if not value or not isinstance(value, str):
            return value
        
        issues = []
        
        # TODO: STUDENT TASK 1
        # Check for contradictions if enabled
        if self.check_contradictions:
            # TODO: Call self._check_contradictions(value) and add any issues
            pass
        
        # TODO: STUDENT TASK 2  
        # Check mathematical consistency if enabled
        if self.check_math:
            # TODO: Call self._check_mathematical_consistency(value) and add any issues
            pass
        
        # TODO: STUDENT TASK 3
        # Check causal relationships if enabled
        if self.check_causality:
            # TODO: Call self._check_causality(value) and add any issues
            pass
        
        # TODO: If any issues found, raise ValidationError
        if issues:
            # TODO: Create comprehensive error message from all issues
            pass
        
        return value
    
    def _check_contradictions(self, text: str) -> List[str]:
        """
        Check for logical contradictions in the text.
        
        TODO: STUDENT TASK 4
        # Use self.contradiction_patterns to find contradictions
        # Return list of contradiction descriptions
        # YOUR CODE HERE:
        """
        contradictions = []
        text_lower = text.lower()
        
        for pattern, description in self.contradiction_patterns:
            # TODO: Use re.search to find pattern matches
            # If found, add description to contradictions list
            pass
        
        # TODO: ADVANCED - Check for numeric contradictions
        # Example: "The price increased from $100 to $80" (increase but lower number)
        
        return contradictions
    
    def _check_mathematical_consistency(self, text: str) -> List[str]:
        """
        Check for mathematical inconsistencies.
        
        TODO: STUDENT TASK 5
        # Find and validate mathematical expressions
        # Check calculations like "2 + 2 = 5" (should be 4)
        # Check percentages, ratios, and basic arithmetic
        # YOUR CODE HERE:
        """
        math_issues = []
        
        # TODO: Pattern 1 - Simple additions: "X + Y = Z"
        addition_pattern = r'(\d+)\s*\+\s*(\d+)\s*=\s*(\d+)'
        # TODO: Use re.findall to find all matches
        # For each match, check if the calculation is correct
        # If not, add to math_issues
        
        # TODO: Pattern 2 - Simple subtractions: "X - Y = Z"
        
        # TODO: Pattern 3 - Simple multiplications: "X * Y = Z" or "X × Y = Z"
        
        # TODO: Pattern 4 - Percentage calculations
        # Example: "50% of 100 is 60" (should be 50)
        percentage_pattern = r'(\d+)%\s+of\s+(\d+)\s+is\s+(\d+)'
        # TODO: Implement percentage validation
        
        return math_issues
    
    def _check_causality(self, text: str) -> List[str]:
        """
        Check for causal relationship inconsistencies.
        
        TODO: STUDENT TASK 6
        # Look for cause-and-effect statements that don't make logical sense
        # Example: "Because it's raining, the ground is dry"
        # YOUR CODE HERE:
        """
        causality_issues = []
        
        # Define some basic cause-effect relationships
        positive_relationships = {
            "rain": ["wet", "flooding", "puddles"],
            "heat": ["hot", "warm", "melting", "evaporation"],
            "cold": ["freezing", "ice", "snow"],
            "exercise": ["fitness", "strength", "health"],
        }
        
        negative_relationships = {
            "rain": ["dry", "drought"],
            "heat": ["cold", "freezing"],
            "cold": ["hot", "warm"],
            "exercise": ["weakness", "laziness"],
        }
        
        # TODO: Look for causal patterns like "because X" followed by contradictory effects
        causal_patterns = [
            r'because\s+.*?(rain|raining).*?(dry|drought)',
            r'due to\s+.*?(heat|hot).*?(cold|freezing)',
            r'since\s+.*?(exercise|exercising).*?(weak|lazy)',
        ]
        
        for pattern in causal_patterns:
            # TODO: Use re.search to find causal contradictions
            # Add appropriate descriptions to causality_issues
            pass
        
        return causality_issues
    
    def _extract_numbers_from_text(self, text: str) -> List[Tuple[str, float]]:
        """
        Helper method to extract numbers and their context from text.
        
        TODO: STUDENT TASK 7 (HELPER METHOD)
        # Extract numbers along with their surrounding context
        # Return list of (context, number) tuples
        # YOUR CODE HERE:
        """
        numbers = []
        
        # TODO: Use regex to find numbers in context
        # Pattern could be: r'([^.]*?)(\d+(?:\.\d+)?)([^.]*?)'
        # This gives context before and after each number
        
        return numbers


def create_logic_guard(**kwargs) -> LogicCheckGuard:
    """Factory function to create a logic check guard."""
    return LogicCheckGuard(**kwargs)


# Test scenarios for students to validate their implementation
def test_logic_check():
    """Test function for students to verify their implementation."""
    
    print("🧪 Testing Logic Check Guardrail")
    print("=" * 50)
    
    # Test case 1: Contradiction detection
    contradiction_guard = create_logic_guard(
        check_contradictions=True,
        check_math=False,
        check_causality=False
    )
    
    test_cases_1 = [
        ("The weather is always sunny, but sometimes it rains.", "SHOULD_FAIL"),
        ("All birds can fly, but some birds cannot fly.", "SHOULD_FAIL"),
        ("It's impossible to travel faster than light, but it's possible with new technology.", "SHOULD_FAIL"),
        ("The population increased dramatically and decreased significantly.", "SHOULD_FAIL"),
        ("The weather is usually sunny, and occasionally it rains.", "SHOULD_PASS"),
    ]
    
    print("\n📝 Test 1: Contradiction Detection")
    _run_logic_test_cases(contradiction_guard, test_cases_1)
    
    # Test case 2: Mathematical consistency
    math_guard = create_logic_guard(
        check_contradictions=False,
        check_math=True,
        check_causality=False
    )
    
    test_cases_2 = [
        ("The calculation shows that 2 + 2 = 4.", "SHOULD_PASS"),
        ("We found that 5 + 3 = 7.", "SHOULD_FAIL"),  # Wrong math
        ("The result is 10 - 4 = 6.", "SHOULD_PASS"),
        ("According to our analysis, 3 × 4 = 15.", "SHOULD_FAIL"),  # Wrong math
        ("The percentage shows that 25% of 100 is 25.", "SHOULD_PASS"),
        ("We calculated that 50% of 80 is 50.", "SHOULD_FAIL"),  # Should be 40
    ]
    
    print("\n📝 Test 2: Mathematical Consistency")
    _run_logic_test_cases(math_guard, test_cases_2)
    
    # Test case 3: Causality checks
    causality_guard = create_logic_guard(
        check_contradictions=False,
        check_math=False,
        check_causality=True
    )
    
    test_cases_3 = [
        ("Because it's raining heavily, the ground is completely wet.", "SHOULD_PASS"),
        ("Due to the rain, everything outside is dry.", "SHOULD_FAIL"),
        ("Since it's very hot outside, the ice cream melted quickly.", "SHOULD_PASS"),
        ("Because of the intense heat, the water froze solid.", "SHOULD_FAIL"),
        ("Since he exercises regularly, he has become quite fit.", "SHOULD_PASS"),
    ]
    
    print("\n📝 Test 3: Causality Checks")
    _run_logic_test_cases(causality_guard, test_cases_3)


def _run_logic_test_cases(guard: LogicCheckGuard, test_cases: List[tuple]):
    """Helper function to run logic test cases."""
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
    
    1. Complete the TODO sections in the LogicCheckGuard class
    2. Start with contradiction detection (Tasks 1 and 4)
    3. Then implement mathematical consistency (Tasks 2 and 5)
    4. Finally add causality checking (Tasks 3 and 6)
    5. Run this file to test: python 03_logic_check.py
    6. All tests should pass with appropriate PASS/BLOCK results
    
    HINTS:
    ------
    - For contradictions: Use re.search() with the predefined patterns
    - For math: Extract numbers with regex, then validate calculations
    - For causality: Look for "because/due to/since" followed by contradictory outcomes
    - Use re.findall() to extract multiple matches
    - Remember to handle edge cases and invalid inputs
    
    LOGICAL PATTERNS TO DETECT:
    --------------------------
    1. Contradictions:
       - "always" vs "sometimes"
       - "all" vs "some...not" 
       - "impossible" vs "possible"
       - Directional contradictions (increase vs decrease)
    
    2. Mathematical errors:
       - Wrong arithmetic: "2 + 2 = 5"
       - Incorrect percentages: "50% of 100 is 60"
       - Basic calculation mistakes
    
    3. Causal inconsistencies:
       - "Because it rains, everything is dry"
       - "Due to heat, water froze"
       - Cause-effect contradictions
    
    EXTENSION CHALLENGES:
    --------------------
    - Add support for more complex mathematical expressions
    - Implement temporal logic checking (before/after consistency)
    - Add probability logic validation
    - Create domain-specific logic rules (physics, economics, etc.)
    - Implement fuzzy logic for handling partial contradictions
    """
    test_logic_check()