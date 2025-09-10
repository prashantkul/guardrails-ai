# 🛡️ Enhanced Financial Compliance System with AI Guardrails

A comprehensive **financial compliance validation system** featuring advanced NLP analysis, custom guardrails, and an interactive Gradio web interface for real-time financial content compliance checking.

🌐 [Guardrails AI Hub](https://hub.guardrailsai.com/) | 📚 [Documentation](https://docs.guardrailsai.com/)

## 🎯 What This System Provides

### 🏦 **Enhanced Financial Advisor** - Production-Ready Application
- **🧠 Advanced NLP Analysis**: Powered by spaCy custom NER for linguistic context awareness
- **🛡️ Multi-Layer Compliance**: Pattern matching + guardrails + advanced entity detection
- **🎨 Beautiful Visualization**: Color-coded compliance analysis with detailed explanations
- **📊 Multi-Page Interface**: Separate Chat and Compliance Analysis tabs for optimal UX
- **🔄 Real-Time Validation**: Instant prompt and response compliance checking

### 🧪 **Advanced Detection Capabilities**
- **Financial Risk Entities**: Guarantee language, risk-free claims, insider information
- **Linguistic Context**: Understanding of phrase boundaries and word relationships  
- **Regulatory Compliance**: SEC/FINRA aligned validation patterns
- **Educational Features**: Learn compliance through interactive examples
- **Smart Enhancements**: Automatic conversion of risky language to compliant alternatives

### 🎓 **Learning Components** - Educational Resources
- **Interactive Tutorials**: Progressive learning with hands-on guardrail implementation
- **Custom Validator Examples**: Production-ready financial compliance patterns
- **Comprehensive Documentation**: Detailed guides and usage examples

## 🛠️ Setup

### Prerequisites
- Python 3.11+
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

3. **Download spaCy language model:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Configure API keys:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

   Required API keys:
   - `GEMINI_API_KEY` or `GOOGLE_API_KEY`: For Google Gemini LLM
   - `GROQ_API_KEY`: For LLM-based analysis (optional)

## 🚀 Usage

### 🏦 **Enhanced Financial Advisor** - Main Application

**Launch the Interactive Web Interface:**
```bash
python gradio_financial_advisor.py
```

Features:
- **💬 Chat Tab**: Ask financial questions with real-time compliance checking
- **📊 Compliance Analysis Tab**: View detailed violation analysis with color highlighting
- **🎛️ AI Response Modes**: Choose from Simple, Compliant, Strict, or Educational modes
- **🧠 Advanced NLP**: spaCy-powered entity detection and linguistic analysis

**Test Questions to Try:**
```
"What's a guaranteed risk-free way to make quick money?"
"Should I invest all my money in Bitcoin for guaranteed profits?"
"Tell me a secret insider tip for the stock market"
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

### 🔧 **Custom Guardrails Demo**

**View Available Validators** - See production-ready implementations:
```bash
cd guardrails_custom
python demo_runner.py --list
```

**Run Financial Compliance Demo** - See comprehensive validation in action:
```bash
python demo_runner.py --validator financial
```

**Interactive Testing** - Test your own content:
```bash
python demo_runner.py --interactive
```

**Architecture Overview** - Learn validator design patterns:
```bash
python demo_runner.py --architecture
```

**Interactive Financial Advisor** - Create compliant financial content with AI assistance:
```bash
python interactive_financial_advisor.py
```
Features:
- Real-time validation of financial content
- AI-powered enhancement with proper disclaimers
- Educational tips and compliant phrase examples
- Save compliant content to file

## 📁 Project Structure

```
guardrails-ai/
├── 🏦 Main Financial Compliance System
│   ├── gradio_financial_advisor.py     # 🚀 Main Gradio web application
│   ├── financial_advisor_prompts.py    # 🎛️ AI response mode management
│   ├── spacy_financial_ner.py          # 🧠 Advanced NLP entity recognition
│   └── requirements.txt                # 📦 Python dependencies (includes spaCy)
│
├── 🛡️ guardrails_custom/              # Custom compliance validators
│   ├── financial_compliance_validator.py  # 📋 Enhanced validator with spaCy
│   ├── interactive_financial_advisor.py   # 💬 Terminal-based advisor
│   └── demo_runner.py                   # 🎯 Validator demonstrations
│
├── 🎓 guardrails_tutorials/           # Educational learning system
│   ├── tutorial_runner.py              # 📚 Interactive tutorial interface
│   ├── exercises/                      # 🧪 Student exercises (TODO sections)
│   │   ├── 01_ban_list.py
│   │   ├── 02_valid_json.py
│   │   ├── 03_logic_check.py
│   │   ├── 04_saliency_check.py
│   │   ├── 05_restrict_to_topic.py
│   │   ├── 06_exclude_sql_predicates.py
│   │   └── 07_grounded_ai_hallucination.py
│   └── solutions/                      # ✅ Complete implementations
│
├── 🏛️ guardrails_showcase/           # Legacy demonstration system
│   ├── basic/                          # 🔰 Basic guardrail examples
│   ├── advanced/                       # 🎯 Advanced patterns
│   └── main_demo.py                    # 🎬 Showcase demonstrations
│
├── 📋 Documentation & Guides
│   ├── README.md                       # 📖 This comprehensive guide
│   ├── COMPLIANCE_VISUALIZATION_FEATURES.md  # 🎨 Visualization documentation
│   ├── demo_multipage_interface.py     # 📱 Interface demonstration
│   └── .env.example                    # 🔐 Environment configuration template
```

## 🧠 Advanced NLP Features (spaCy Integration)

### 🎯 **Enhanced Financial Risk Detection**

The system now features **state-of-the-art NLP analysis** powered by spaCy custom Named Entity Recognition:

#### **🏷️ Custom Financial Risk Entities**
- **GUARANTEE_LANG**: Guaranteed return language (`"guarantee profit"`, `"assured returns"`)
- **RISK_FREE_CLAIM**: Risk-free investment claims (`"risk-free"`, `"no risk"`, `"zero risk"`)  
- **GET_RICH_QUICK**: Get-rich-quick schemes (`"quick money"`, `"overnight success"`)
- **INSIDER_INFO**: Insider trading references (`"secret tips"`, `"insider information"`)
- **NO_LOSS_CLAIM**: Cannot lose promises (`"cannot lose"`, `"impossible to fail"`)

#### **🎨 Visual Entity Recognition**
```python
# Example: "What's a guaranteed risk-free way to make quick money?"
# Results in highlighted entities:
# [guaranteed] (GUARANTEE_LANG - HIGH RISK - RED)
# [risk-free] (RISK_FREE_CLAIM - HIGH RISK - RED)  
# [quick money] (GET_RICH_QUICK - MEDIUM RISK - ORANGE)
```

#### **🔍 Linguistic Context Awareness**
Unlike simple regex patterns, spaCy understands:
- **Word boundaries**: Distinguishes "risk-free" from "low-risk environment"
- **Phrase units**: Recognizes "quick money" as a single semantic unit
- **Context sensitivity**: Differentiates "insider tips" from "helpful tips"
- **Token relationships**: Understands linguistic dependencies between words

### 🏗️ **Technical Architecture**

#### **Three-Layer Validation System:**

1. **🔍 Pattern Layer**: Fast regex-based detection for obvious violations
2. **🛡️ Guardrails Layer**: Comprehensive financial compliance validation
3. **🧠 NLP Layer**: Advanced spaCy entity recognition with linguistic context

#### **Integration Flow:**
```python
# Enhanced validation pipeline
prompt -> spaCy NER -> Guardrails Validator -> Enhanced HTML -> User
         ↓              ↓                      ↓
    Entity Detection   Rule Validation    Color Highlighting
    Risk Assessment    Fix Suggestions    Educational Content
```

#### **Performance Optimizations:**
- **Lazy Loading**: spaCy model loads only when enhanced analysis is enabled
- **Graceful Fallback**: System works with basic patterns if spaCy unavailable  
- **Efficient Caching**: Entity ruler patterns cached for repeated use
- **Fast Inference**: <100ms typical analysis time for financial text

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
- `GEMINI_API_KEY` or `GOOGLE_API_KEY`: API key for Google Gemini LLM
- `GROQ_API_KEY`: API key for Groq LLM services (optional)
- `GUARDRAILS_API_KEY`: API key for Guardrails AI platform (optional)

### Dependencies Included
- **guardrails-ai**: Core validation framework
- **gradio**: Web interface framework  
- **google-generativeai**: Google Gemini integration
- **spacy**: Advanced NLP and entity recognition
- **transformers + torch**: Advanced AI model support (optional)

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

### 🏦 **Enhanced Financial Advisor Results**

**High-Risk Question Analysis:**
```
Input: "What's a guaranteed risk-free way to make quick money?"

🚨 Prompt Violations Detected:
- [guaranteed] (GUARANTEE_LANG - HIGH RISK)
- [risk-free] (RISK_FREE_CLAIM - HIGH RISK)  
- [quick money] (GET_RICH_QUICK - MEDIUM RISK)

📊 Compliance Analysis Generated:
- 16,986 character detailed HTML analysis
- Color-coded entity highlighting
- Side-by-side original vs compliant comparison
- Educational explanations and safer alternatives

🧠 Advanced NLP Analysis:
- HIGH risk (3 entities detected)
- Linguistic context awareness enabled
- spaCy entity recognition successful
```

**Clean Question Analysis:**
```
Input: "Can you explain how diversification works?"

✅ No Violations Detected:
- Compliant educational question
- No problematic financial language
- Appropriate for learning content

📋 Response Enhancement:
- Added educational disclaimers
- Enhanced with professional guidance
- Maintained educational focus
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

By exploring this enhanced financial compliance system, you will master:

### **🛠️ Core Technical Skills**
- ✅ **Advanced NLP**: spaCy custom NER, entity recognition, linguistic pattern matching
- ✅ **Multi-layer Validation**: Pattern matching + guardrails + entity detection
- ✅ **API Integration**: Google Gemini, Groq LLM services, and AI model management
- ✅ **Web Development**: Gradio multi-page interfaces, real-time validation
- ✅ **Financial Compliance**: SEC/FINRA regulatory patterns and requirements

### **🧠 Advanced AI Safety Concepts**
- ✅ **Entity-Level Analysis**: Named Entity Recognition for compliance detection
- ✅ **Linguistic Context**: Understanding phrase boundaries and semantic relationships
- ✅ **Risk Assessment**: Multi-level risk scoring and confidence measurement
- ✅ **Automated Enhancement**: Converting risky language to compliant alternatives
- ✅ **Visual Compliance**: Color-coded analysis and educational explanations

### **📈 Professional Development Skills**
- ✅ **Production-Ready Systems**: Scalable architecture with graceful fallbacks
- ✅ **User Experience Design**: Multi-page interfaces with beautiful visualizations
- ✅ **Educational Technology**: Interactive learning through compliance examples
- ✅ **Regulatory Technology**: Real-world fintech compliance implementation
- ✅ **Advanced Integration**: Combining multiple AI/NLP technologies effectively

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

## 🎉 Get Started Today!

### **🚀 Quick Start - Enhanced Financial Advisor**
```bash
# 1. Setup environment
conda activate guardrails-ai
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# 2. Configure API key
echo 'GEMINI_API_KEY=your_key_here' > .env

# 3. Launch the enhanced system
python gradio_financial_advisor.py
```

### **🧪 Test Advanced Features**
Try these questions to see the full power of spaCy + Guardrails:
- `"What's a guaranteed way to get rich quick with insider tips?"`
- `"Should I invest all my money for risk-free guaranteed profits?"`
- `"Tell me a secret strategy that cannot lose money"`

### **🎯 What You'll Experience**
- **🧠 Advanced NLP**: State-of-the-art entity recognition and linguistic analysis
- **🎨 Beautiful Visualizations**: Color-coded compliance analysis with detailed explanations  
- **📊 Professional Interface**: Multi-page design with separate chat and analysis tabs
- **🛡️ Multi-Layer Protection**: Pattern matching + guardrails + entity detection
- **📚 Educational Value**: Learn compliance through interactive examples

**Build safer, compliant AI systems with cutting-edge NLP technology! 🛡️🧠🚀**