# 🛡️ Guardrails AI Tutorials

**Interactive hands-on tutorials for learning to implement AI safety guardrails**

This comprehensive tutorial series teaches you to build various types of guardrails from scratch, covering everything from basic pattern matching to advanced AI hallucination detection.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Basic understanding of Python and regex
- Conda environment `guardrails-ai` (recommended)

### Setup
1. **Activate your environment:**
   ```bash
   conda activate guardrails-ai
   ```

2. **Install dependencies:**
   ```bash
   pip install -r ../requirements.txt
   ```

3. **Start learning:**
   ```bash
   python tutorial_runner.py --list
   ```

## 📚 Tutorial Catalog

### 🟢 **Beginner Level**

#### **Tutorial 1: Ban List Guardrail** ⭐☆☆
- **Concepts:** Pattern matching, case sensitivity, word boundaries
- **Learn:** How to block content containing banned words/phrases
- **Skills:** Regex, string manipulation, flexible filtering
- **File:** `exercises/01_ban_list.py`

### 🟡 **Intermediate Level**

#### **Tutorial 2: Valid JSON Guardrail** ⭐⭐☆  
- **Concepts:** JSON parsing, error handling, format fixing
- **Learn:** Validate and automatically fix malformed JSON
- **Skills:** JSON manipulation, error recovery, format standardization
- **File:** `exercises/02_valid_json.py`

#### **Tutorial 5: Restrict to Topic Guardrail** ⭐⭐☆
- **Concepts:** Topic classification, keyword matching, LLM integration  
- **Learn:** Keep AI responses within specified topic boundaries
- **Skills:** Text classification, semantic matching, API integration
- **File:** `exercises/05_restrict_to_topic.py`

#### **Tutorial 6: Exclude SQL Predicates Guardrail** ⭐⭐☆
- **Concepts:** SQL injection patterns, security validation, syntax analysis
- **Learn:** Prevent SQL injection attempts and malicious queries
- **Skills:** Security patterns, injection detection, safe filtering
- **File:** `exercises/06_exclude_sql_predicates.py`

### 🔴 **Advanced Level**

#### **Tutorial 3: Logic Check Guardrail** ⭐⭐⭐
- **Concepts:** Contradiction detection, math validation, causality checking
- **Learn:** Detect logical inconsistencies and validate reasoning
- **Skills:** Logic analysis, mathematical verification, causal reasoning
- **File:** `exercises/03_logic_check.py`

#### **Tutorial 4: Saliency Check Guardrail** ⭐⭐⭐  
- **Concepts:** Keyword importance, content focus, relevance scoring
- **Learn:** Ensure content focuses on important/relevant topics
- **Skills:** Content analysis, importance weighting, focus measurement
- **File:** `exercises/04_saliency_check.py`

#### **Tutorial 7: Grounded AI Hallucination Detection** ⭐⭐⭐
- **Concepts:** Fact checking, uncertainty analysis, knowledge base verification
- **Learn:** Detect AI hallucinations using grounding techniques  
- **Skills:** Fact verification, confidence analysis, knowledge grounding
- **File:** `exercises/07_grounded_ai_hallucination.py`

## 🎯 Learning Path Recommendations

### **For Beginners:**
```
Tutorial 1 → Tutorial 2 → Tutorial 6 → Tutorial 5
```
Start with basic concepts, then move to intermediate topics.

### **For Intermediate Users:**
```  
Tutorial 1 → Tutorial 5 → Tutorial 3 → Tutorial 4
```
Focus on classification and analysis techniques.

### **For Advanced Users:**
```
Tutorial 3 → Tutorial 4 → Tutorial 7 → Custom Implementation
```
Master complex analysis and create your own guardrails.

## 🛠️ How to Use

### **Running Tutorials**

```bash
# Show all available tutorials
python tutorial_runner.py --list

# Run a specific tutorial  
python tutorial_runner.py --tutorial 1

# View solution for tutorial
python tutorial_runner.py --solution 1

# Check progress
python tutorial_runner.py --progress
```

### **Tutorial Structure**

Each tutorial follows this pattern:

1. **📖 Introduction** - Objective and learning goals
2. **🎯 Concepts** - Key concepts you'll learn  
3. **📝 Implementation** - TODO sections for you to complete
4. **🧪 Testing** - Built-in test cases to validate your work
5. **💡 Hints** - Guidance and best practices
6. **🚀 Extensions** - Advanced challenges to try

### **Working with TODO Sections**

Each tutorial contains `TODO: STUDENT TASK` comments:

```python
# TODO: STUDENT TASK 1
# Implement the validation logic here
# YOUR CODE HERE:
def validate(self, value: str) -> str:
    # TODO: Add your implementation
    pass
```

**Your job:** Replace the `pass` statements with working code!

## 📁 Project Structure

```
guardrails_tutorials/
├── README.md                    # This file
├── tutorial_runner.py           # Main tutorial interface
├── exercises/                   # Tutorial exercises (your playground)
│   ├── 01_ban_list.py
│   ├── 02_valid_json.py
│   ├── 03_logic_check.py
│   ├── 04_saliency_check.py
│   ├── 05_restrict_to_topic.py
│   ├── 06_exclude_sql_predicates.py
│   └── 07_grounded_ai_hallucination.py
└── solutions/                   # Complete solutions (for reference)
    ├── 01_ban_list_solution.py
    ├── 02_valid_json_solution.py
    └── ... (solutions for all tutorials)
```

## 🎓 Learning Objectives

By completing these tutorials, you will learn:

### **Core Skills:**
- ✅ Pattern matching and regex techniques
- ✅ Content validation and sanitization  
- ✅ Error handling and recovery strategies
- ✅ API integration with LLM services
- ✅ Security-focused input validation

### **Advanced Concepts:**
- ✅ Logical consistency checking
- ✅ Semantic content analysis
- ✅ AI hallucination detection
- ✅ Knowledge base integration
- ✅ Confidence and uncertainty quantification

### **Best Practices:**
- ✅ Defensive programming techniques
- ✅ Comprehensive error handling
- ✅ Performance optimization strategies
- ✅ Testing and validation approaches
- ✅ Documentation and maintainability

## 🔧 Development Tips

### **Getting Started:**
1. Always read the tutorial introduction completely
2. Understand the test cases before implementing  
3. Start with the simplest TODO tasks first
4. Run tests frequently to check your progress
5. Don't hesitate to check solutions if stuck

### **Debugging:**
```bash
# Run individual tutorial files directly
python exercises/01_ban_list.py

# Enable verbose output in tests
# Look for test functions that accept verbose parameters
```

### **Testing Your Implementation:**
```python
# Each tutorial has built-in test functions
def test_tutorial_name():
    # Test cases with expected results
    test_cases = [
        ("input text", "SHOULD_PASS"),
        ("blocked text", "SHOULD_FAIL"),
    ]
    # Run tests and see results
```

## 🌟 Extension Ideas

After completing the tutorials, try these challenges:

### **Integration Projects:**
- Combine multiple guardrails into a pipeline
- Create a web API for guardrails validation
- Build a real-time content moderation system
- Integrate with popular AI frameworks

### **Advanced Features:**
- Add machine learning-based classification
- Implement multi-language support
- Create custom domain-specific guardrails
- Add monitoring and analytics capabilities

### **Performance Optimizations:**
- Implement caching for repeated validations
- Add async/await support for LLM calls
- Create batched processing capabilities
- Optimize regex patterns for speed

## 🤝 Contributing

Want to add more tutorials or improve existing ones?

1. Fork the repository
2. Create a new tutorial following the established pattern
3. Include comprehensive TODO sections and test cases
4. Provide both exercise and solution versions
5. Update this README with your tutorial
6. Submit a pull request

### **Tutorial Template:**
```python
"""
TUTORIAL X: Your Guardrail Name
===============================

OBJECTIVE: Clear description of what students will learn

LEARNING GOALS:
- Goal 1
- Goal 2  
- Goal 3

DIFFICULTY: ⭐⭐☆ (Appropriate level)
"""

# Your tutorial implementation with TODO sections
```

## 📖 Additional Resources

### **Related Documentation:**
- [Guardrails AI Official Docs](https://docs.guardrailsai.com/)
- [Pattern Matching Best Practices](https://regex101.com/)
- [Python Security Guidelines](https://python.org/dev/security/)

### **Academic Papers:**
- "AI Safety via Debate" (OpenAI, 2018)
- "Constitutional AI" (Anthropic, 2022)  
- "Training Language Models to Follow Instructions" (OpenAI, 2022)

### **Community:**
- Join discussions on AI safety and guardrails
- Share your custom implementations
- Get help with challenging concepts

## 🎉 Conclusion

These tutorials provide a solid foundation for implementing robust AI safety guardrails. Start with the basics, progress through intermediate concepts, and master advanced techniques.

**Happy learning, and build safer AI systems! 🛡️🤖**

---

*Need help? Found a bug? Have suggestions? Please open an issue or contribute to the project!*