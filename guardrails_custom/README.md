# 🛡️ Custom Guardrails - Production-Ready Validators

Advanced, professional-grade custom validators demonstrating the full power of the Guardrails AI framework. These implementations follow official Guardrails AI patterns and are suitable for production use.

## 🎯 Overview

This module contains sophisticated custom validators that showcase:
- **Professional Architecture**: Following `@register_validator` patterns
- **Multi-Stage Validation**: Complex validation workflows
- **LLM Integration**: AI-powered analysis and enhancement
- **Production Features**: Error handling, fallbacks, and fixes
- **Real-World Applications**: Ready for deployment in production systems

## 📦 Available Validators

### 1. Financial Compliance Validator

A comprehensive validator ensuring financial content meets regulatory requirements (SEC/FINRA guidelines).

**Features:**
- ✅ Multi-stage validation (topic detection → compliance checking)
- ✅ Detects and blocks guaranteed return language
- ✅ Requires proper disclaimers for financial advice
- ✅ Flags overly specific predictions without uncertainty
- ✅ LLM integration for advanced analysis
- ✅ Automatic fix suggestions

**Use Cases:**
- Investment advice platforms
- Financial content moderation
- Regulatory compliance automation
- Risk management for fintech apps
- Social media financial content
- Newsletter and blog compliance

## 🚀 Quick Start

### Installation

Ensure you have the Guardrails AI environment set up:
```bash
conda activate guardrails-ai
pip install -r ../requirements.txt
```

### Basic Usage

#### 1. Import and Use the Validator

```python
from guardrails_custom.financial_compliance_validator import FinancialComplianceValidator

# Create validator instance
validator = FinancialComplianceValidator(
    require_disclaimers=True,
    check_guaranteed_returns=True,
    check_specific_predictions=True,
    strict_compliance=False
)

# Validate content
content = "Buy AAPL stock for guaranteed 50% returns!"
result = validator._validate(content, {})

if hasattr(result, 'error_message'):
    print(f"❌ Failed: {result.error_message}")
    print(f"✨ Fix: {result.fix_value}")
else:
    print("✅ Passed validation")
```

#### 2. Use with Guardrails Guard

```python
from guardrails import Guard
from guardrails_custom.financial_compliance_validator import FinancialComplianceValidator

# Create guard with validator
guard = Guard()
guard.use(FinancialComplianceValidator(
    require_disclaimers=True,
    check_guaranteed_returns=True
))

# Validate content
try:
    result = guard.validate("Invest now for guaranteed profits!")
except Exception as e:
    print(f"Validation failed: {e}")
```

## 🎮 Interactive Tools

### 1. Demo Runner

Explore all available validators and their capabilities:

```bash
# Show available validators
python demo_runner.py --list

# Run financial validator demo
python demo_runner.py --validator financial

# Interactive testing mode
python demo_runner.py --interactive

# Learn about validator architecture
python demo_runner.py --architecture
```

### 2. Interactive Financial Advisor

A powerful tool for creating compliant financial content:

```bash
python interactive_financial_advisor.py
```

**Features:**
- 📝 Real-time content validation
- 🤖 AI-powered compliance enhancement
- 📚 Educational tips and best practices
- ✨ Automatic disclaimer addition
- 💾 Save compliant content to file

**Menu Options:**
1. **Validate Your Content** - Check if your financial text is compliant
2. **AI Enhancement** - Transform non-compliant content automatically
3. **Compliance Tips** - Learn what to do and avoid
4. **Example Phrases** - See compliant language examples
5. **Test Samples** - Try pre-loaded test cases

## 📋 Example Transformations

### Before (Non-Compliant)
```
"This stock will double your money in 30 days guaranteed!"
```

### After (Compliant)
```
"This stock has shown growth potential, though past performance 
doesn't guarantee future results. Returns may vary and all 
investments carry risk. This is not financial advice - please 
consult a financial professional."
```

## 🏗️ Validator Architecture

### Structure
```
@register_validator(name="financial-compliance", data_type="string")
class FinancialComplianceValidator(Validator):
    def _validate(self, value: str, metadata: Dict) -> ValidationResult:
        # Multi-stage validation logic
        # Returns PassResult() or FailResult(error_message, fix_value)
```

### Key Components

1. **Topic Detection**
   - Identifies financial content using keyword matching
   - Determines if compliance rules should apply

2. **Pattern Matching**
   - Regex patterns for prohibited language
   - Detection of missing disclaimers
   - Identification of specific predictions

3. **LLM Integration**
   - Advanced compliance checking via Groq API
   - Intelligent content enhancement
   - Fallback to rule-based methods

4. **Fix Suggestions**
   - Automatic disclaimer addition
   - Language softening (guaranteed → potentially)
   - Uncertainty injection for predictions

## 🧪 Testing

### Run Validator Tests
```python
# Run the demo to see all test cases
python demo_runner.py --validator financial
```

### Test Cases Include:
- ✅ Content with proper disclaimers
- ❌ Guaranteed return language
- ❌ Risk-free investment claims
- ❌ Specific price predictions
- ❌ Missing disclaimers on advice
- ✅ Non-financial content (passes through)

## 🎯 Real-World Applications

### Primary Use Case: LLM Output Validation

The Financial Compliance Validator is primarily designed to ensure AI-generated financial content is compliant before being shown to users.

### Key Applications

1. **AI Financial Advisors**
   - Validate LLM-generated investment advice before serving to users
   - Ensure chatbot responses include required disclaimers
   - Filter out prohibited guarantee language from AI outputs

2. **Automated Content Generation**
   - Validate AI-written financial articles before publication
   - Ensure AI-generated newsletters are compliant
   - Check robo-advisor recommendations for regulatory compliance

3. **Fintech AI Applications**
   - Filter AI trading insights before displaying to users
   - Validate AI market analysis for compliance
   - Ensure AI-generated reports include risk warnings

4. **Customer Support AI**
   - Validate AI agent responses about financial products
   - Ensure automated emails include proper disclaimers
   - Check AI-generated FAQ responses for compliance

## 🔧 Configuration Options

### Validator Parameters

```python
FinancialComplianceValidator(
    require_disclaimers=True,      # Enforce disclaimer requirements
    check_guaranteed_returns=True,  # Block guarantee language
    check_specific_predictions=True, # Flag specific predictions
    check_unlicensed_advice=True,   # Detect unlicensed advice
    use_llm_verification=True,      # Enable LLM analysis
    strict_compliance=False         # Strictness level
)
```

## 📚 Compliance Rules

### Prohibited Language
- ❌ "Guaranteed returns/profits"
- ❌ "Risk-free investment"
- ❌ "Cannot lose money"
- ❌ "Will definitely increase"
- ❌ Specific price/date predictions

### Required Elements
- ✅ Disclaimers ("Not financial advice")
- ✅ Risk warnings
- ✅ Uncertainty language ("might", "could")
- ✅ Professional consultation mentions

## 🔄 Integration Examples

### Primary Pattern: Validating LLM Output

```python
from openai import OpenAI
from guardrails_custom.financial_compliance_validator import FinancialComplianceValidator

client = OpenAI()
validator = FinancialComplianceValidator()

def get_financial_advice(user_question: str) -> str:
    # 1. Get response from LLM
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_question}]
    )
    
    llm_output = response.choices[0].message.content
    
    # 2. Validate LLM output BEFORE showing to user
    result = validator._validate(llm_output, {})
    
    # 3. Return compliant version to user
    if hasattr(result, 'error_message'):
        # Use the auto-fixed version
        return result.fix_value
    else:
        # Already compliant
        return llm_output

# Example usage
user_question = "What stocks should I buy?"
safe_response = get_financial_advice(user_question)
# Response will always include disclaimers and avoid prohibited language
```

### With FastAPI (AI Chatbot Backend)
```python
from fastapi import FastAPI
from guardrails_custom.financial_compliance_validator import FinancialComplianceValidator
import openai

app = FastAPI()
validator = FinancialComplianceValidator()

@app.post("/chat")
async def chat(message: str):
    # Generate AI response
    ai_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}]
    )
    
    llm_output = ai_response.choices[0].message.content
    
    # Validate and fix LLM output
    result = validator._validate(llm_output, {})
    
    if hasattr(result, 'error_message'):
        # Return fixed version with compliance
        return {"response": result.fix_value, "modified": True}
    else:
        # Return original (already compliant)
        return {"response": llm_output, "modified": False}
```

### With Streamlit (AI Financial Assistant)
```python
import streamlit as st
from guardrails_custom.financial_compliance_validator import FinancialComplianceValidator
import openai

validator = FinancialComplianceValidator()

st.title("AI Financial Assistant")
user_input = st.text_input("Ask a financial question:")

if st.button("Get Advice"):
    with st.spinner("Generating response..."):
        # Get LLM response
        llm_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        ).choices[0].message.content
        
        # Validate LLM output
        result = validator._validate(llm_response, {})
        
        if hasattr(result, 'error_message'):
            st.warning("⚠️ Response modified for compliance")
            st.write(result.fix_value)
        else:
            st.write(llm_response)
```

## 🤝 Contributing

To add new custom validators:

1. Create a new validator class inheriting from `Validator`
2. Implement the `_validate()` method
3. Use `@register_validator` decorator
4. Add demo cases to `demo_runner.py`
5. Create interactive tools if applicable

## 📄 License

This project is part of the Guardrails AI educational platform. Use these validators as templates for building your own production validators.

## 🔗 Resources

- [Guardrails AI Documentation](https://docs.guardrailsai.com/)
- [Guardrails Hub](https://hub.guardrailsai.com/)
- [Custom Validator Guide](https://www.guardrailsai.com/docs/how_to_guides/custom_validators)

## 💡 Next Steps

1. **Explore**: Run the demos to understand validator capabilities
2. **Learn**: Study the implementation patterns
3. **Customize**: Modify validators for your specific needs
4. **Deploy**: Integrate into your production systems
5. **Extend**: Create new validators for other domains

---

Built with ❤️ for the Guardrails AI community