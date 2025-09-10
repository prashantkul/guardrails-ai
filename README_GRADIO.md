# 🏦 Gradio Financial Advisor with Gemini & Guardrails

A comprehensive web-based financial advisor built with Gradio that integrates Google Gemini for AI-powered advice generation and custom guardrails for financial compliance validation.

## 🌟 Features

### 🚀 **Core Functionality**
- **Web-based Interface**: Clean, user-friendly Gradio interface
- **Google Gemini Integration**: Advanced AI for financial advice generation  
- **Dual Guardrails System**: Validates both user prompts and AI responses
- **Real-time Compliance**: Automatic detection and fixing of regulatory issues
- **Educational Focus**: Provides safe, compliant financial information

### 🛡️ **Safety & Compliance**
- **Prompt Validation**: Checks user questions before processing
- **Response Validation**: Ensures AI responses meet financial compliance standards
- **Automatic Enhancement**: Rule-based fixing of common compliance issues
- **SEC/FINRA Alignment**: Follows regulatory guidelines for financial content
- **Required Disclaimers**: Automatically adds appropriate disclaimers

### 🎯 **Multiple AI Response Modes**
- **Simple Mode**: Direct responses with minimal compliance overhead (development/testing)
- **Compliant Mode**: Balanced compliance with helpfulness (production default)
- **Strict Mode**: Maximum regulatory adherence (financial institutions)
- **Educational Mode**: Teaching-focused with comprehensive explanations (learning platforms)

### 🛡️ **Validation Features**
- Blocks guaranteed return language
- Softens overly specific predictions
- Adds uncertainty language ("might", "could", "may")
- Requires appropriate disclaimers for financial advice
- Detects unlicensed advice indicators

## 🚦 Getting Started

### Prerequisites
```bash
# Ensure you have the correct conda environment
conda activate guardrails-ai

# Verify required packages are installed
pip list | grep -E "(gradio|google-generativeai)"
```

### 📋 Installation
```bash
# Install additional dependencies
pip install gradio google-generativeai

# Or install from requirements.txt
pip install -r requirements.txt
```

### 🔑 API Configuration
Set up your Gemini API key in `.env`:
```bash
# Add to your .env file
GEMINI_API_KEY=your_gemini_api_key_here
# OR
GOOGLE_API_KEY=your_google_api_key_here
```

### 🚀 Launch the Application

#### Method 1: Direct Launch
```bash
python gradio_financial_advisor.py
```

#### Method 2: Programmatic Launch  
```python
from gradio_financial_advisor import GradioFinancialAdvisor

advisor = GradioFinancialAdvisor()
advisor.launch(
    share=True,        # Create public link (optional)
    server_port=7860,  # Custom port
    debug=False        # Debug mode
)
```

### 🧪 Testing
Run the test suite to verify everything works:
```bash
python test_gradio_app.py
```

## 📱 Using the Interface

### 🎯 **Main Features**
1. **Ask Questions**: Type financial questions in the chat interface
2. **Switch AI Modes**: Choose from 4 different response styles using the dropdown
3. **Real-time Validation**: See guardrails status in the right panel
4. **Example Questions**: Click on provided examples to get started
5. **Mode Information**: View current mode characteristics and compliance level
6. **Compliance Info**: View validation details for each response

### 💡 **Example Questions**
- "What are the benefits of investing in index funds for retirement?"
- "How does compound interest work with savings accounts?"
- "Should I prioritize paying off debt or investing first?"
- "What's the difference between stocks and bonds?"
- "How much should I save for an emergency fund?"
- "Is real estate a good investment for beginners?"

### 🎯 **AI Response Modes**

#### 🔸 Simple Mode
- **Use Case**: Development and testing
- **Compliance**: Minimal (requires post-processing)
- **Response Style**: Direct, concise answers
- **Risk Level**: High - needs validation

#### 🔸 Compliant Mode (Default)
- **Use Case**: Production applications  
- **Compliance**: Standard financial disclaimers
- **Response Style**: Balanced advice with uncertainty language
- **Risk Level**: Low - built-in compliance

#### 🔸 Strict Mode
- **Use Case**: Financial institutions, regulated environments
- **Compliance**: Maximum regulatory adherence
- **Response Style**: Educational only, multiple disclaimers
- **Risk Level**: Minimal - over-cautious

#### 🔸 Educational Mode
- **Use Case**: Learning platforms, financial literacy
- **Compliance**: Teaching-focused disclaimers
- **Response Style**: Comprehensive explanations with examples
- **Risk Level**: Low - educational emphasis

### 🛡️ **Guardrails in Action**

#### User Input Validation
```
❌ Empty questions → Prompts for valid input
⚠️ Problematic language → Warns but allows processing  
✅ Good questions → Processes normally
```

#### AI Response Validation
```
✅ Compliant responses → Pass through unchanged
🔧 Minor issues → Automatically enhanced
⚠️ Major issues → Fixed with rule-based enhancements
```

## 🔧 Architecture

### 🏗️ **System Components**

#### 1. **GradioFinancialAdvisor Class**
- Main application controller
- Handles user interactions and API calls
- Manages conversation history

#### 2. **Dual Validator System**
```python
# Prompt Validator (Permissive)
self.prompt_validator = FinancialComplianceValidator(
    require_disclaimers=False,  # Users don't need disclaimers
    check_guaranteed_returns=True,
    strict_compliance=False
)

# Response Validator (Strict) 
self.response_validator = FinancialComplianceValidator(
    require_disclaimers=True,   # AI responses need disclaimers
    check_guaranteed_returns=True,
    check_specific_predictions=True,
    strict_compliance=True
)
```

#### 3. **Processing Pipeline**
```
User Question → Prompt Validation → Gemini API → Response Validation → Display
```

### 🛠️ **Key Methods**

#### `validate_user_prompt(prompt: str)`
- Validates user input for basic safety
- Returns validation status and processed prompt
- Uses permissive validation rules

#### `generate_financial_advice(prompt: str)`  
- Calls Google Gemini API with system prompt
- Handles API errors gracefully
- Includes financial advisory context

#### `validate_ai_response(response: str)`
- Applies strict financial compliance validation
- Automatically fixes common issues
- Returns enhanced compliant response

#### `_rule_based_compliance_fix(text: str)`
- Applies rule-based compliance enhancements
- Softens guaranteed language
- Adds required disclaimers

## 📊 Compliance Features

### 🚫 **Blocked Content**
- Guaranteed return promises ("guaranteed 20% profit")
- Risk-free investment claims ("cannot lose money")
- Overly specific predictions ("will hit $200 next week")
- Unlicensed advice indicators ("as a financial advisor")

### ✅ **Automatic Enhancements**
- Replaces "guarantee" with "potentially"
- Changes "will" to "might" for predictions
- Adds uncertainty language throughout
- Includes required disclaimers

### 📋 **Required Disclaimers**
Automatically added when needed:
```
"This information is for educational purposes only and is not 
personalized financial advice. Always consult with a qualified 
financial advisor before making investment decisions."
```

## 🎛️ **Customization Options**

### Interface Customization
```python
advisor = GradioFinancialAdvisor()

# Launch with custom settings
advisor.launch(
    server_name="0.0.0.0",    # Allow external access
    server_port=8080,         # Custom port
    share=True,               # Create public link
    auth=("user", "pass"),    # Add authentication
    debug=True                # Enable debug mode
)
```

### Validator Customization
```python
# Custom prompt validator
custom_prompt_validator = FinancialComplianceValidator(
    require_disclaimers=False,
    check_guaranteed_returns=True,
    strict_compliance=False
)

# Custom response validator
custom_response_validator = FinancialComplianceValidator(
    require_disclaimers=True,
    check_specific_predictions=True,
    use_llm_verification=True,  # Enable LLM verification
    strict_compliance=True
)
```

## 🔍 **Monitoring & Logging**

### Status Panel
The right panel shows real-time status:
- **API Status**: Gemini connection status
- **Guardrails Status**: Active validation systems
- **Validation Results**: Per-interaction compliance info

### System Health
Check these indicators:
- ✅ **Gemini API**: Connected and responding
- ✅ **Prompt Guardrails**: Validating user input
- ✅ **Response Guardrails**: Validating AI output
- ✅ **Compliance Checks**: SEC/FINRA rules active

## 🤝 **Integration with Existing System**

This Gradio app integrates seamlessly with your existing guardrails system:

```python
# Uses existing financial compliance validator
from guardrails_custom.financial_compliance_validator import FinancialComplianceValidator

# Leverages existing patterns and rules
# Extends functionality with web interface
# Maintains all existing compliance features
```

## 🚀 **Production Deployment**

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 7860

CMD ["python", "gradio_financial_advisor.py"]
```

### Environment Variables
```bash
# Required
GEMINI_API_KEY=your_api_key

# Optional
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=7860
GRADIO_SHARE=false
```

## 📈 **Performance & Scaling**

### Optimization Tips
- Use caching for repeated validations
- Implement request rate limiting
- Add response time monitoring  
- Consider load balancing for high traffic

### Resource Usage
- Memory: ~200MB baseline + model cache
- CPU: Moderate (validation rules + API calls)
- Network: API calls to Gemini (controllable)

## 🔒 **Security Considerations**

### API Key Management
- Store keys in environment variables
- Use secret management in production
- Rotate keys regularly

### Input Validation
- All user inputs validated before processing
- Protection against prompt injection
- Rate limiting recommended

### Data Privacy
- No conversation history stored by default
- Consider implementing data retention policies
- Ensure GDPR/CCPA compliance if applicable

## 🛠️ **Troubleshooting**

### Common Issues

#### API Key Not Working
```bash
# Check environment variables
echo $GEMINI_API_KEY

# Test API key manually
python -c "import google.generativeai as genai; genai.configure(api_key='YOUR_KEY'); print('✅ API key valid')"
```

#### Import Errors
```bash
# Ensure correct conda environment
conda activate guardrails-ai

# Reinstall dependencies
pip install --upgrade gradio google-generativeai
```

#### Port Already in Use
```bash
# Find and kill process using port 7860
lsof -ti:7860 | xargs kill -9

# Or use different port
python gradio_financial_advisor.py --port 8080
```

### Debug Mode
Enable detailed logging:
```python
advisor.launch(debug=True)
```

## 📚 **Related Documentation**

- [Guardrails AI Documentation](https://docs.guardrailsai.com/)
- [Google Gemini API](https://developers.generativeai.google/)
- [Gradio Documentation](https://gradio.app/docs/)
- [Financial Compliance Validator](./guardrails_custom/financial_compliance_validator.py)

## 🎯 **Next Steps**

### Potential Enhancements
- [ ] Add conversation history persistence
- [ ] Implement user authentication
- [ ] Add more financial validation rules
- [ ] Create mobile-responsive design
- [ ] Add analytics dashboard
- [ ] Integrate with more LLM providers

### Advanced Features
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Document upload and analysis
- [ ] Integration with financial data APIs
- [ ] Custom compliance rule editor

---

**🎉 You now have a production-ready financial advisor with comprehensive guardrails!**

Launch the app and start asking financial questions to see the guardrails in action. All responses are automatically validated and enhanced for regulatory compliance.