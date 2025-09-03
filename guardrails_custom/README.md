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

### Use Cases

1. **Investment Platforms**
   - Validate user-generated investment advice
   - Ensure forum posts are compliant
   - Moderate financial discussions

2. **Content Creation**
   - Blog post compliance checking
   - Newsletter validation
   - Social media post verification

3. **Fintech Applications**
   - Robo-advisor communication compliance
   - Trading app notification validation
   - Investment recommendation checking

4. **Educational Platforms**
   - Ensure course content includes disclaimers
   - Validate instructor communications
   - Check student forum posts

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

### With FastAPI
```python
from fastapi import FastAPI, HTTPException
from guardrails_custom.financial_compliance_validator import FinancialComplianceValidator

app = FastAPI()
validator = FinancialComplianceValidator()

@app.post("/validate-content")
async def validate_content(text: str):
    result = validator._validate(text, {})
    if hasattr(result, 'error_message'):
        raise HTTPException(400, detail=result.error_message)
    return {"status": "compliant", "text": text}
```

### With Streamlit
```python
import streamlit as st
from guardrails_custom.financial_compliance_validator import FinancialComplianceValidator

validator = FinancialComplianceValidator()

st.title("Financial Content Validator")
user_input = st.text_area("Enter financial content:")

if st.button("Validate"):
    result = validator._validate(user_input, {})
    if hasattr(result, 'error_message'):
        st.error(f"❌ {result.error_message}")
        st.success(f"✨ Suggestion: {result.fix_value}")
    else:
        st.success("✅ Content is compliant!")
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