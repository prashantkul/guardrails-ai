"""
TUTORIAL 4: Saliency Check Guardrail
=====================================

OBJECTIVE: Create a guardrail that ensures AI responses focus on the most important/relevant content.

LEARNING GOALS:
- Understand content saliency and relevance scoring
- Implement keyword importance weighting
- Detect off-topic or irrelevant content
- Calculate content focus scores

DIFFICULTY: ⭐⭐⭐ (Advanced)
"""

import re
from typing import List, Dict, Set, Tuple
from collections import Counter
from guardrails.errors import ValidationError


class SaliencyCheckGuard:
    """
    A guardrail that validates content saliency and relevance.
    
    TODO: Students will implement saliency checking methods.
    """
    
    def __init__(self, important_keywords: List[str] = None, 
                 min_saliency_score: float = 0.3, 
                 max_irrelevant_ratio: float = 0.4,
                 check_focus: bool = True):
        """
        Initialize the saliency check guardrail.
        
        Args:
            important_keywords: List of keywords that should be emphasized
            min_saliency_score: Minimum required saliency score (0.0 to 1.0)
            max_irrelevant_ratio: Maximum allowed ratio of irrelevant content
            check_focus: Whether to check content focus and coherence
        """
        self.important_keywords = [kw.lower() for kw in (important_keywords or [])]
        self.min_saliency_score = min_saliency_score
        self.max_irrelevant_ratio = max_irrelevant_ratio
        self.check_focus = check_focus
        
        # Common stop words to filter out
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
    
    def validate(self, value: str) -> str:
        """
        Validate the saliency and relevance of content.
        
        Args:
            value: Input text to validate
            
        Returns:
            str: Original value if saliency requirements are met
            
        Raises:
            ValidationError: If content fails saliency checks
        """
        if not value or not isinstance(value, str):
            return value
        
        # TODO: STUDENT TASK 1
        # Calculate the overall saliency score
        # Call self._calculate_saliency_score(value)
        saliency_score = 0.0  # TODO: Implement this
        
        # TODO: STUDENT TASK 2
        # Calculate content focus metrics
        if self.check_focus:
            # TODO: Call self._check_content_focus(value)
            # This should return focus_score and issues list
            focus_score, focus_issues = 0.0, []  # TODO: Implement this
        else:
            focus_score, focus_issues = 1.0, []
        
        # TODO: STUDENT TASK 3
        # Validate against thresholds and raise errors if needed
        issues = []
        
        # TODO: Check if saliency_score < self.min_saliency_score
        # TODO: Add focus_issues to issues list
        # TODO: If any issues, raise ValidationError
        
        return value
    
    def _calculate_saliency_score(self, text: str) -> float:
        """
        Calculate the saliency score of the text based on important keywords.
        
        TODO: STUDENT TASK 4
        # Calculate how much the text focuses on important topics
        # Higher score = more salient content
        # Score range: 0.0 to 1.0
        # YOUR CODE HERE:
        """
        if not self.important_keywords:
            return 1.0  # If no keywords specified, assume content is salient
        
        words = self._extract_words(text)
        if not words:
            return 0.0
        
        # TODO: Count occurrences of important keywords
        important_word_count = 0
        total_word_count = len(words)
        
        for word in words:
            # TODO: Check if word is in self.important_keywords
            # If so, increment important_word_count
            pass
        
        # TODO: Calculate and return saliency score
        # Formula: important_word_count / total_word_count
        # But also consider keyword density and variety
        
        return 0.0  # TODO: Replace with actual calculation
    
    def _check_content_focus(self, text: str) -> Tuple[float, List[str]]:
        """
        Check how focused and coherent the content is.
        
        TODO: STUDENT TASK 5
        # Analyze content focus using various metrics:
        # 1. Topic consistency
        # 2. Sentence coherence
        # 3. Repetition patterns
        # 4. Tangent detection
        # YOUR CODE HERE:
        """
        issues = []
        sentences = self._split_into_sentences(text)
        
        if len(sentences) == 0:
            return 0.0, ["No sentences found"]
        
        # TODO: Metric 1 - Check for topic consistency
        # Calculate similarity between sentences
        topic_consistency_score = 0.0  # TODO: Implement
        
        # TODO: Metric 2 - Check for excessive repetition
        repetition_score = self._check_repetition(text)
        
        # TODO: Metric 3 - Check for tangential content
        # Detect sentences that seem unrelated to main topic
        tangent_score = 0.0  # TODO: Implement
        
        # TODO: Combine scores into overall focus score
        focus_score = 0.0  # TODO: Calculate from metrics above
        
        # TODO: Add issues based on low scores
        if topic_consistency_score < 0.5:
            issues.append("Low topic consistency detected")
        
        if repetition_score < 0.3:
            issues.append("Excessive repetition detected")
        
        return focus_score, issues
    
    def _extract_words(self, text: str) -> List[str]:
        """
        Extract meaningful words from text, filtering out stop words.
        
        TODO: STUDENT TASK 6
        # Extract words and filter out stop words and punctuation
        # Convert to lowercase for consistency
        # YOUR CODE HERE:
        """
        # TODO: Use regex to extract words (letters only)
        # TODO: Convert to lowercase
        # TODO: Filter out stop words
        # TODO: Return list of meaningful words
        
        words = []
        # TODO: Implement word extraction
        return words
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences.
        
        TODO: STUDENT TASK 7
        # Split text by sentence boundaries
        # YOUR CODE HERE:
        """
        # TODO: Split by sentence-ending punctuation
        # TODO: Clean up empty sentences
        sentences = []
        # TODO: Implement sentence splitting
        return sentences
    
    def _check_repetition(self, text: str) -> float:
        """
        Check for excessive repetition in content.
        
        TODO: STUDENT TASK 8
        # Calculate a score for content repetition
        # Lower score = more repetitive content
        # Score range: 0.0 to 1.0
        # YOUR CODE HERE:
        """
        words = self._extract_words(text)
        if len(words) < 2:
            return 1.0
        
        # TODO: Count word frequencies
        word_counts = {}  # TODO: Use Counter or dict
        
        # TODO: Calculate repetition metrics
        # Consider: word frequency distribution, repeated phrases
        
        # TODO: Return score where 1.0 = no repetition, 0.0 = highly repetitive
        return 1.0  # TODO: Replace with actual calculation
    
    def _calculate_sentence_similarity(self, sent1: str, sent2: str) -> float:
        """
        Calculate similarity between two sentences (simple word overlap method).
        
        TODO: STUDENT TASK 9 (ADVANCED)
        # Calculate similarity using word overlap
        # Score range: 0.0 to 1.0
        # YOUR CODE HERE:
        """
        words1 = set(self._extract_words(sent1))
        words2 = set(self._extract_words(sent2))
        
        if not words1 or not words2:
            return 0.0
        
        # TODO: Calculate Jaccard similarity or similar metric
        # Jaccard = intersection / union
        
        return 0.0  # TODO: Replace with actual calculation


def create_saliency_guard(**kwargs) -> SaliencyCheckGuard:
    """Factory function to create a saliency check guard."""
    return SaliencyCheckGuard(**kwargs)


# Test scenarios for students to validate their implementation
def test_saliency_check():
    """Test function for students to verify their implementation."""
    
    print("🧪 Testing Saliency Check Guardrail")
    print("=" * 50)
    
    # Test case 1: Keyword-based saliency
    keyword_guard = create_saliency_guard(
        important_keywords=["machine learning", "AI", "algorithm", "model", "data"],
        min_saliency_score=0.2,
        check_focus=False
    )
    
    test_cases_1 = [
        ("Machine learning algorithms are essential for AI model development using data.", "SHOULD_PASS"),
        ("The weather is nice today and I like ice cream very much.", "SHOULD_FAIL"),
        ("Our AI model uses advanced machine learning techniques to analyze data patterns.", "SHOULD_PASS"),
        ("Yesterday I went shopping and bought some groceries for dinner.", "SHOULD_FAIL"),
        ("Data science involves algorithms and machine learning for AI applications.", "SHOULD_PASS"),
    ]
    
    print("\n📝 Test 1: Keyword-based Saliency")
    _run_saliency_test_cases(keyword_guard, test_cases_1)
    
    # Test case 2: Content focus checking
    focus_guard = create_saliency_guard(
        important_keywords=["technology", "innovation", "software"],
        min_saliency_score=0.1,
        check_focus=True
    )
    
    test_cases_2 = [
        ("Technology innovation drives software development forward.", "SHOULD_PASS"),
        ("Technology technology technology software software innovation.", "SHOULD_FAIL"),  # Repetitive
        ("Software innovation is important. Technology helps us grow. Innovation drives progress.", "SHOULD_PASS"),
        ("The cat sat on the mat. Dogs like bones. Fish swim in water.", "SHOULD_FAIL"),  # Unfocused
    ]
    
    print("\n📝 Test 2: Content Focus Checking")
    _run_saliency_test_cases(focus_guard, test_cases_2)
    
    # Test case 3: Combined saliency and focus
    comprehensive_guard = create_saliency_guard(
        important_keywords=["business", "strategy", "growth", "market"],
        min_saliency_score=0.3,
        max_irrelevant_ratio=0.3,
        check_focus=True
    )
    
    test_cases_3 = [
        ("Business strategy focuses on market growth through innovative approaches.", "SHOULD_PASS"),
        ("Our business strategy aims for sustainable market growth.", "SHOULD_PASS"), 
        ("I like pizza and movies. The sky is blue today.", "SHOULD_FAIL"),  # Low saliency
        ("Business business business strategy strategy market growth.", "SHOULD_FAIL"),  # Repetitive
    ]
    
    print("\n📝 Test 3: Comprehensive Saliency and Focus")
    _run_saliency_test_cases(comprehensive_guard, test_cases_3)


def _run_saliency_test_cases(guard: SaliencyCheckGuard, test_cases: List[tuple]):
    """Helper function to run saliency test cases."""
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
    
    1. Complete the TODO sections in the SaliencyCheckGuard class
    2. Start with basic saliency scoring (Tasks 1, 4, and 6)
    3. Then implement content focus checking (Tasks 2, 5, 7-9)
    4. Finally integrate all checks (Task 3)
    5. Run this file to test: python 04_saliency_check.py
    6. All tests should pass with appropriate PASS/BLOCK results
    
    HINTS:
    ------
    - For word extraction: use re.findall(r'\\b[a-zA-Z]+\\b', text.lower())
    - For saliency: count important keywords vs total words
    - For repetition: use Counter to count word frequencies
    - For sentence splitting: use re.split(r'[.!?]+', text)
    - For similarity: use Jaccard index (intersection/union of word sets)
    
    SALIENCY CONCEPTS:
    ------------------
    1. Keyword Density: How often important terms appear
    2. Topic Consistency: How well content stays on topic
    3. Focus Score: Measures coherence and relevance
    4. Repetition Analysis: Detects excessive repetition
    5. Tangent Detection: Identifies off-topic content
    
    SCORING FORMULAS:
    ----------------
    - Saliency Score = important_keywords_count / total_words_count
    - Focus Score = average of (consistency + variety + relevance)
    - Repetition Score = 1.0 - (repetition_penalty)
    
    EXTENSION CHALLENGES:
    --------------------
    - Add TF-IDF scoring for better keyword weighting
    - Implement topic modeling for semantic similarity
    - Add named entity recognition for content analysis
    - Create domain-specific saliency models
    - Implement attention mechanisms for importance weighting
    """
    test_saliency_check()