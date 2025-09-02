"""
TUTORIAL 5: Restrict to Topic Guardrail
========================================

OBJECTIVE: Create a guardrail that ensures AI responses stay on a specific topic.

LEARNING GOALS:
- Implement topic classification and validation
- Use keyword-based and semantic topic detection
- Handle topic drift and off-topic content
- Create flexible topic boundaries

DIFFICULTY: ⭐⭐☆ (Intermediate)
"""

import os
import re
from typing import List, Set, Dict, Optional
from collections import Counter
from dotenv import load_dotenv
import requests
from guardrails.errors import ValidationError

load_dotenv()


class RestrictToTopicGuard:
    """
    A guardrail that restricts content to specific topics.
    
    TODO: Students will implement topic restriction methods.
    """
    
    def __init__(self, allowed_topics: List[str], 
                 topic_keywords: Dict[str, List[str]] = None,
                 min_topic_relevance: float = 0.3,
                 use_llm_classification: bool = True,
                 strict_mode: bool = False):
        """
        Initialize the topic restriction guardrail.
        
        Args:
            allowed_topics: List of allowed topic names
            topic_keywords: Dict mapping topic names to their associated keywords
            min_topic_relevance: Minimum relevance score for topic matching
            use_llm_classification: Whether to use LLM for topic classification
            strict_mode: If True, be strict about topic adherence
        """
        self.allowed_topics = [topic.lower() for topic in allowed_topics]
        self.topic_keywords = self._normalize_topic_keywords(topic_keywords or {})
        self.min_topic_relevance = min_topic_relevance
        self.use_llm_classification = use_llm_classification
        self.strict_mode = strict_mode
        
        # Default keywords for common topics if not provided
        self._add_default_keywords()
    
    def validate(self, value: str) -> str:
        """
        Validate that content stays within allowed topics.
        
        Args:
            value: Input text to validate
            
        Returns:
            str: Original value if topic requirements are met
            
        Raises:
            ValidationError: If content is off-topic
        """
        if not value or not isinstance(value, str):
            return value
        
        if not self.allowed_topics:
            return value  # No restrictions if no topics specified
        
        # TODO: STUDENT TASK 1
        # Calculate topic scores using keyword-based method
        # Call self._calculate_keyword_topic_scores(value)
        keyword_scores = {}  # TODO: Implement this
        
        # TODO: STUDENT TASK 2
        # If LLM classification is enabled, get LLM topic scores
        llm_scores = {}
        if self.use_llm_classification:
            # TODO: Call self._get_llm_topic_classification(value)
            pass
        
        # TODO: STUDENT TASK 3
        # Combine scores and determine final topic classification
        # Call self._combine_topic_scores(keyword_scores, llm_scores)
        final_scores = {}  # TODO: Implement this
        
        # TODO: STUDENT TASK 4
        # Check if any allowed topic meets the minimum relevance threshold
        # If not, raise ValidationError
        max_score = 0.0
        best_topic = None
        
        # TODO: Find the highest scoring allowed topic
        # TODO: Check if max_score >= self.min_topic_relevance
        # TODO: If not, raise ValidationError with details
        
        return value
    
    def _calculate_keyword_topic_scores(self, text: str) -> Dict[str, float]:
        """
        Calculate topic relevance scores based on keyword matching.
        
        TODO: STUDENT TASK 5
        # For each allowed topic, calculate how relevant the text is
        # based on keyword matching
        # YOUR CODE HERE:
        """
        scores = {}
        text_words = self._extract_words(text)
        
        if not text_words:
            return {topic: 0.0 for topic in self.allowed_topics}
        
        for topic in self.allowed_topics:
            # TODO: Get keywords for this topic
            topic_keywords = self.topic_keywords.get(topic, [])
            
            if not topic_keywords:
                scores[topic] = 0.0
                continue
            
            # TODO: Count how many topic keywords appear in the text
            keyword_matches = 0
            for keyword in topic_keywords:
                # TODO: Check if keyword appears in text_words
                # Handle both single words and phrases
                pass
            
            # TODO: Calculate relevance score
            # Formula: keyword_matches / max(len(topic_keywords), len(text_words))
            scores[topic] = 0.0  # TODO: Replace with actual calculation
        
        return scores
    
    def _get_llm_topic_classification(self, text: str) -> Dict[str, float]:
        """
        Use LLM to classify text into topics.
        
        TODO: STUDENT TASK 6
        # Use Groq API to classify the text into allowed topics
        # Return a dict with topic names and confidence scores
        # YOUR CODE HERE:
        """
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            return {}
        
        # TODO: Create a prompt for topic classification
        topics_str = ", ".join(self.allowed_topics)
        prompt = f"""
        Classify the following text into one or more of these topics: {topics_str}
        
        For each topic, provide a relevance score from 0.0 to 1.0.
        
        Text: "{text}"
        
        Respond in this format:
        topic1: score1
        topic2: score2
        ...
        """
        
        try:
            # TODO: Make API call to Groq
            # TODO: Parse the response to extract topic scores
            # TODO: Return dict of {topic: score}
            pass
        except Exception as e:
            # If LLM fails, return empty scores
            return {}
    
    def _combine_topic_scores(self, keyword_scores: Dict[str, float], 
                             llm_scores: Dict[str, float]) -> Dict[str, float]:
        """
        Combine keyword-based and LLM-based topic scores.
        
        TODO: STUDENT TASK 7
        # Combine the two scoring methods intelligently
        # YOUR CODE HERE:
        """
        combined_scores = {}
        
        for topic in self.allowed_topics:
            keyword_score = keyword_scores.get(topic, 0.0)
            llm_score = llm_scores.get(topic, 0.0)
            
            # TODO: Combine scores using a weighted average or other method
            # Consider: keyword_score has weight 0.4, llm_score has weight 0.6
            # Or use max, average, or other combination strategy
            
            combined_scores[topic] = 0.0  # TODO: Replace with actual combination
        
        return combined_scores
    
    def _extract_words(self, text: str) -> List[str]:
        """
        Extract words from text for keyword matching.
        
        TODO: STUDENT TASK 8
        # Extract meaningful words from text
        # YOUR CODE HERE:
        """
        # TODO: Use regex to extract words
        # TODO: Convert to lowercase
        # TODO: Filter out very short words
        words = []
        # TODO: Implement word extraction
        return words
    
    def _normalize_topic_keywords(self, topic_keywords: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """
        Normalize topic keywords to lowercase.
        
        TODO: STUDENT TASK 9
        # Convert all topic names and keywords to lowercase
        # YOUR CODE HERE:
        """
        normalized = {}
        for topic, keywords in topic_keywords.items():
            # TODO: Convert topic name to lowercase
            # TODO: Convert all keywords to lowercase
            # TODO: Add to normalized dict
            pass
        return normalized
    
    def _add_default_keywords(self):
        """
        Add default keywords for common topics if not provided.
        
        TODO: STUDENT TASK 10
        # Add default keywords for topics that don't have any
        # YOUR CODE HERE:
        """
        default_keywords = {
            "technology": ["computer", "software", "digital", "tech", "internet", "AI", "programming"],
            "health": ["medical", "doctor", "hospital", "medicine", "treatment", "patient", "disease"],
            "business": ["company", "market", "profit", "sales", "strategy", "management", "finance"],
            "science": ["research", "study", "experiment", "data", "analysis", "theory", "discovery"],
            "sports": ["game", "team", "player", "match", "score", "competition", "athlete"],
            "politics": ["government", "policy", "election", "politician", "law", "vote", "democracy"],
            "education": ["school", "student", "teacher", "learning", "university", "education", "study"],
        }
        
        for topic in self.allowed_topics:
            # TODO: If topic doesn't have keywords, add defaults if available
            if topic not in self.topic_keywords and topic in default_keywords:
                # TODO: Add default keywords for this topic
                pass


def create_topic_guard(allowed_topics: List[str], **kwargs) -> RestrictToTopicGuard:
    """Factory function to create a topic restriction guard."""
    return RestrictToTopicGuard(allowed_topics, **kwargs)


# Test scenarios for students to validate their implementation
def test_restrict_to_topic():
    """Test function for students to verify their implementation."""
    
    print("🧪 Testing Restrict to Topic Guardrail")
    print("=" * 50)
    
    # Test case 1: Technology topic restriction
    tech_guard = create_topic_guard(
        allowed_topics=["technology"],
        min_topic_relevance=0.3,
        use_llm_classification=False
    )
    
    test_cases_1 = [
        ("The new software update includes AI features and better programming tools.", "SHOULD_PASS"),
        ("I love pizza and ice cream for dinner every day.", "SHOULD_FAIL"),
        ("Digital transformation is changing how companies use technology.", "SHOULD_PASS"),
        ("The weather is nice today and flowers are blooming.", "SHOULD_FAIL"),
        ("Computer programming requires understanding of algorithms and data structures.", "SHOULD_PASS"),
    ]
    
    print("\n📝 Test 1: Technology Topic Restriction")
    _run_topic_test_cases(tech_guard, test_cases_1)
    
    # Test case 2: Multiple allowed topics
    multi_guard = create_topic_guard(
        allowed_topics=["health", "science"],
        topic_keywords={
            "health": ["medical", "doctor", "patient", "treatment", "hospital"],
            "science": ["research", "study", "experiment", "data", "analysis"]
        },
        min_topic_relevance=0.2,
        use_llm_classification=False
    )
    
    test_cases_2 = [
        ("Medical research shows new treatment options for patients.", "SHOULD_PASS"),
        ("The scientific study analyzed data from multiple experiments.", "SHOULD_PASS"),
        ("I went shopping for groceries and bought some vegetables.", "SHOULD_FAIL"),
        ("Hospital doctors are conducting research on new treatments.", "SHOULD_PASS"),
        ("The movie was entertaining with great special effects.", "SHOULD_FAIL"),
    ]
    
    print("\n📝 Test 2: Multiple Allowed Topics")
    _run_topic_test_cases(multi_guard, test_cases_2)
    
    # Test case 3: Strict mode testing
    strict_guard = create_topic_guard(
        allowed_topics=["business"],
        min_topic_relevance=0.5,  # Higher threshold
        strict_mode=True,
        use_llm_classification=False
    )
    
    test_cases_3 = [
        ("Our company's marketing strategy focuses on increasing sales and profit.", "SHOULD_PASS"),
        ("The business meeting discussed financial management and market analysis.", "SHOULD_PASS"),
        ("Some people like to travel and explore new places.", "SHOULD_FAIL"),
        ("The market research shows positive trends for our business strategy.", "SHOULD_PASS"),
        ("Today is a beautiful day with sunshine and blue skies.", "SHOULD_FAIL"),
    ]
    
    print("\n📝 Test 3: Strict Mode Testing")
    _run_topic_test_cases(strict_guard, test_cases_3)


def _run_topic_test_cases(guard: RestrictToTopicGuard, test_cases: List[tuple]):
    """Helper function to run topic test cases."""
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
    
    1. Complete the TODO sections in the RestrictToTopicGuard class
    2. Start with keyword-based topic scoring (Tasks 5, 8-10)
    3. Then implement the main validation logic (Tasks 1, 3-4)
    4. Optionally implement LLM classification (Tasks 2, 6-7)
    5. Run this file to test: python 05_restrict_to_topic.py
    6. All tests should pass with appropriate PASS/BLOCK results
    
    HINTS:
    ------
    - For keyword matching: check if words/phrases appear in text
    - For topic scoring: count matching keywords vs total keywords
    - For word extraction: use re.findall(r'\\b[a-zA-Z]+\\b', text.lower())
    - For phrase matching: check if multi-word keywords appear as substrings
    - Handle both single words and multi-word phrases in keywords
    
    TOPIC CLASSIFICATION APPROACHES:
    -------------------------------
    1. Keyword-based: Count relevant keywords for each topic
    2. LLM-based: Use AI model to classify content into topics
    3. Combined: Weighted average of keyword and LLM scores
    4. Semantic similarity: Compare text to topic descriptions (advanced)
    
    SCORING STRATEGIES:
    ------------------
    - Simple count: number of matching keywords
    - Normalized: matches / total_keywords or matches / text_length
    - Weighted: important keywords get higher weights
    - TF-IDF: term frequency-inverse document frequency (advanced)
    
    EXTENSION CHALLENGES:
    --------------------
    - Add semantic similarity using word embeddings
    - Implement topic modeling (LDA, BERT-based)
    - Add hierarchical topic classification (main topic -> subtopics)
    - Create topic drift detection over long conversations
    - Add confidence intervals and uncertainty handling
    """
    test_restrict_to_topic()