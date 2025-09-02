# 🛡️ Guardrails AI Comprehensive Learning System

A complete educational platform for learning AI safety guardrails implementation, featuring both a **showcase demonstration** and **hands-on interactive tutorials**.

🌐 [Guardrails AI Hub](https://hub.guardrailsai.com/) | 📚 [Documentation](https://docs.guardrailsai.com/)

## 🎯 What You'll Learn

This project provides two complementary learning experiences:

### 🏛️ **Guardrails Showcase** - Live Demonstrations
- **Competitor Mention Blocking**: Prevents content from mentioning competitor companies
- **Format Validation**: Enforces exact format requirements (email, phone, specific patterns)
- **Psychological Manipulation Detection**: Identifies manipulative language patterns using both regex and LLM analysis
- **Infrastructure Validation**: Validates URLs, IP addresses, domains, and email domains
- **Logical Fallacy Detection**: Detects common logical fallacies and validates argument structure

### 🎓 **Interactive Tutorials** - Hands-On Learning
- **7 Progressive Tutorials**: From beginner to advanced implementation
- **TODO-Based Learning**: Complete real guardrail implementations step-by-step
- **Built-in Testing**: Validate your solutions with comprehensive test cases
- **Complete Solutions**: Reference implementations for guidance

## 🛠️ Setup

### Prerequisites
- Python 3.12
- Conda environment named `guardrails-ai`

### Installation

1. **Activate the conda environment:**
   ```bash
   conda activate guardrails-ai
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

   Required API keys:
   - `GROQ_API_KEY`: For LLM-based analysis
   - `GUARDRAILS_API_KEY`: For Guardrails AI platform features

## 🎯 Usage

### 🏛️ **Guardrails Showcase Demo**

**Quick Demo** - Run all guardrails demonstrations:
```bash
python main_demo.py
```

**Interactive Mode** - Test your own inputs:
```bash
python main_demo.py --interactive
```

**Specific Demos**:
```bash
# Basic guardrails only
python main_demo.py --basic-only

# Advanced guardrails only
python main_demo.py --advanced-only

# Verbose output
python main_demo.py --verbose
```

### 🎓 **Interactive Tutorial System**

**Start Learning** - See all available tutorials:
```bash
cd guardrails_tutorials
python3 tutorial_runner.py --list
```

**Run a Tutorial** - Work on specific exercises:
```bash
python3 tutorial_runner.py --tutorial 1    # Start with Tutorial 1
python3 tutorial_runner.py --tutorial 7    # Advanced hallucination detection
```

**Check Solutions** - View complete implementations:
```bash
python3 tutorial_runner.py --solution 1    # See solution for Tutorial 1
```

**Track Progress** - Monitor your learning journey:
```bash
python3 tutorial_runner.py --progress
```

## 📁 Project Structure

```
guardrails-ai/
├── 🏛️ guardrails_showcase/           # Live demonstration system
│   ├── basic/
│   │   ├── competitor_blocking.py      # Competitor mention detection
│   │   └── format_validator.py         # Format validation rules
│   ├── advanced/
│   │   ├── psychological_manipulation.py   # Manipulation detection
│   │   ├── infrastructure_validation.py    # URL/IP/domain validation
│   │   └── logical_fallacy_detection.py    # Logical fallacy detection
│   └── utils/
├── 🎓 guardrails_tutorials/           # Interactive learning system
│   ├── tutorial_runner.py              # Main tutorial interface
│   ├── README.md                       # Tutorial documentation
│   ├── exercises/                      # Student exercises (TODO sections)
│   │   ├── 01_ban_list.py
│   │   ├── 02_valid_json.py
│   │   ├── 03_logic_check.py
│   │   ├── 04_saliency_check.py
│   │   ├── 05_restrict_to_topic.py
│   │   ├── 06_exclude_sql_predicates.py
│   │   └── 07_grounded_ai_hallucination.py
│   └── solutions/                      # Complete implementations
│       ├── 01_ban_list_solution.py
│       ├── 02_valid_json_solution.py
│       └── ... (solutions for all tutorials)
├── main_demo.py                        # Main demonstration script
├── requirements.txt                    # Python dependencies
├── .env.example                        # Environment variables template
└── README.md                          # This file
```

## 🎓 Tutorial Learning Path

### **📚 Available Tutorials** (Progressive Difficulty)

#### 🟢 **Beginner Level**
- **Tutorial 1: Ban List Guardrail** ⭐☆☆
  - Pattern matching, case sensitivity, word boundaries
  - Perfect starting point for learning guardrails

#### 🟡 **Intermediate Level**  
- **Tutorial 2: Valid JSON Guardrail** ⭐⭐☆
  - JSON parsing, error handling, format fixing
- **Tutorial 5: Restrict to Topic** ⭐⭐☆
  - Topic classification, keyword matching, LLM integration
- **Tutorial 6: Exclude SQL Predicates** ⭐⭐☆
  - SQL injection patterns, security validation, syntax analysis

#### 🔴 **Advanced Level**
- **Tutorial 3: Logic Check Guardrail** ⭐⭐⭐
  - Contradiction detection, math validation, causality checking
- **Tutorial 4: Saliency Check Guardrail** ⭐⭐⭐
  - Keyword importance, content focus, relevance scoring  
- **Tutorial 7: Grounded AI Hallucination** ⭐⭐⭐
  - Fact checking, uncertainty analysis, knowledge base verification

### **🎯 Recommended Learning Paths**

**For Beginners:**
```
Tutorial 1 → Tutorial 2 → Tutorial 6 → Tutorial 5
```

**For Intermediate Users:**
```
Tutorial 1 → Tutorial 5 → Tutorial 3 → Tutorial 4
```

**For Advanced Users:**
```
Tutorial 3 → Tutorial 4 → Tutorial 7 → Custom Implementation
```

## 🔧 Configuration

### Environment Variables
- `GROQ_API_KEY`: API key for Groq LLM services
- `GUARDRAILS_API_KEY`: API key for Guardrails AI platform
- `HUGGINGFACE_API_TOKEN`: Optional, for Hugging Face models

### Guardrail Configuration Examples

**Competitor Blocking:**
```python
from guardrails_showcase.basic.competitor_blocking import create_competitor_guard

competitors = ["OpenAI", "Google", "Microsoft"]
guard = create_competitor_guard(competitors)
```

**Format Validation:**
```python
from guardrails_showcase.basic.format_validator import create_format_guard

# Two words, all caps
guard = create_format_guard('two_words_caps')

# Custom format
guard = create_format_guard('custom', word_count=3, all_caps=True)
```

**Manipulation Detection:**
```python
from guardrails_showcase.advanced.psychological_manipulation import create_manipulation_guard

guard = create_manipulation_guard()
```

## 📊 Example Outputs

### 🏛️ **Showcase Demo Results**

**Competitor Blocking:**
```
✅ PASSED: "Our AI solution is great for customer service."
❌ BLOCKED: "Unlike OpenAI's GPT, our model is better."
```

**Format Validation:**
```
✅ PASSED: "HELLO WORLD" (two words, all caps)
❌ BLOCKED: "hello world" (not all caps)
```

**Manipulation Detection:**
```
✅ PASSED: "Our product improves productivity."
❌ BLOCKED: "ACT NOW! Limited time - you'll regret missing this!"
```

### 🎓 **Tutorial Learning Experience**

**Tutorial Progress Tracking:**
```bash
$ python3 tutorial_runner.py --progress
================================================================================
📈 TUTORIAL PROGRESS
================================================================================
✅ Tutorial 1: Ban List Guardrail
   📂 Exercise: ✅    🔍 Solution: ✅
✅ Tutorial 2: Valid JSON Guardrail  
   📂 Exercise: ✅    🔍 Solution: ✅
...
```

**Student Exercise Format:**
```python
# TODO: STUDENT TASK 1
# Implement the ban list validation logic here
# YOUR CODE HERE:
def validate(self, value: str) -> str:
    # TODO: Add your implementation
    pass
```

**Test Results:**
```
🧪 Testing Ban List Guardrail
=================================
1. 'Hello, this is a normal message' → ✅ PASSED
2. 'Check out this OpenAI model' → ✅ BLOCKED
   Reason: Banned word detected: openai
```

## 🧪 Testing Individual Components

Each guardrail module includes demo functions:

```python
# Test competitor blocking
from guardrails_showcase.basic.competitor_blocking import demo_competitor_blocking
results = demo_competitor_blocking()

# Test format validation
from guardrails_showcase.basic.format_validator import demo_format_validation
results = demo_format_validation()

# Test manipulation detection
from guardrails_showcase.advanced.psychological_manipulation import demo_manipulation_detection
results = demo_manipulation_detection()
```

## 🎓 Learning Outcomes

By completing this comprehensive learning system, you will master:

### **🛠️ Core Technical Skills**
- ✅ Pattern matching and regex techniques for content filtering
- ✅ JSON parsing, validation, and error recovery
- ✅ API integration with LLM services (Groq)
- ✅ Security-focused input validation and SQL injection prevention
- ✅ Error handling and defensive programming techniques

### **🧠 Advanced AI Safety Concepts**
- ✅ Logical consistency checking and contradiction detection
- ✅ Semantic content analysis and topic classification
- ✅ AI hallucination detection using grounding techniques
- ✅ Confidence scoring and uncertainty quantification
- ✅ Knowledge base integration for fact verification

### **📈 Professional Development Skills**
- ✅ Test-driven development with comprehensive validation
- ✅ Progressive learning through structured exercises  
- ✅ Code documentation and maintainability practices
- ✅ Performance optimization for content validation
- ✅ Real-world application of AI safety principles

## 🌟 Extension Challenges

Ready to go beyond the tutorials? Try these advanced projects:

### **🔗 Integration Projects**
- Combine multiple guardrails into validation pipelines
- Create REST APIs for guardrails as microservices
- Build real-time content moderation systems
- Integrate with popular AI frameworks (LangChain, Haystack)

### **🚀 Advanced Features**  
- Add machine learning-based classification models
- Implement multi-language support for global content
- Create domain-specific guardrails (medical, legal, financial)
- Add monitoring, analytics, and performance dashboards

### **⚡ Performance Optimizations**
- Implement caching for repeated validations
- Add async/await support for concurrent processing
- Create batched processing for high-throughput scenarios
- Optimize regex patterns and algorithms for speed

## 📚 Additional Learning Resources

### **Official Documentation**
- [Guardrails AI Documentation](https://docs.guardrailsai.com/)
- [Pattern-based vs LLM-based Validation](https://docs.guardrailsai.com/concepts/)
- [Custom Validator Development](https://docs.guardrailsai.com/validators/)

### **Academic Research**
- "AI Safety via Debate" (OpenAI, 2018)
- "Constitutional AI" (Anthropic, 2022)
- "Training Language Models to Follow Instructions" (OpenAI, 2022)

### **Community & Support**
- Join AI safety and guardrails discussions
- Share your custom implementations and solutions
- Get help with challenging concepts and advanced techniques

## 🤝 Contributing

We welcome contributions to expand this educational platform!

### **🏛️ Showcase Contributions**
1. Fork the repository
2. Create a feature branch  
3. Add your guardrail implementation to `guardrails_showcase/`
4. Include demo functions and comprehensive tests
5. Update documentation with usage examples
6. Submit a pull request

### **🎓 Tutorial Contributions**
1. Follow the established tutorial template format
2. Create both exercise (with TODO sections) and solution versions
3. Include progressive TODO tasks for student learning
4. Add comprehensive test cases with expected results
5. Update `tutorial_runner.py` with your new tutorial
6. Provide clear learning objectives and difficulty rating

### **Tutorial Template Structure:**
```python
"""
TUTORIAL X: Your Guardrail Name
===============================

OBJECTIVE: Clear description of what students will learn

LEARNING GOALS:
- Goal 1: Specific skill or concept
- Goal 2: Technical implementation detail  
- Goal 3: Real-world application

DIFFICULTY: ⭐⭐⭐ (Appropriate level)
"""

class YourGuardrailClass:
    def validate(self, value: str) -> str:
        # TODO: STUDENT TASK 1
        # Description of what to implement
        # YOUR CODE HERE:
        pass

# Built-in test function
def test_your_guardrail():
    """Test function for students to verify implementation."""
    # Comprehensive test cases here
```

## 🙏 Acknowledgments

This educational platform demonstrates the power of:
- **Guardrails AI** - The foundational framework for AI safety
- **Groq** - Fast LLM inference for real-time validation  
- **Open Source Community** - Collaborative learning and knowledge sharing

## 📄 License

This project is for **educational and demonstration purposes**. 

- ✅ Free to use for learning and teaching
- ✅ Modify and adapt for educational use
- ✅ Share with students and colleagues
- ⚠️ Check individual dependencies for their respective licenses
- ⚠️ Not intended for production use without proper testing and validation

---

**🎉 Start your AI safety journey today! Begin with the showcase demo, then dive deep with hands-on tutorials. Build safer AI systems through practical learning! 🛡️🤖**