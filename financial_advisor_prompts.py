#!/usr/bin/env python3
"""
Financial Advisor System Prompts
================================

Collection of different system prompt versions for testing and comparison.
This allows for easy experimentation with different prompt styles and
compliance levels.
"""

from typing import Dict, Any
from enum import Enum


class PromptVersion(Enum):
    """Available prompt versions."""
    SIMPLE = "simple"
    COMPLIANT = "compliant"
    STRICT = "strict"
    EDUCATIONAL = "educational"


class FinancialAdvisorPrompts:
    """Centralized collection of financial advisor system prompts."""
    
    @staticmethod
    def get_prompt(version: PromptVersion = PromptVersion.COMPLIANT) -> str:
        """
        Get a system prompt by version.
        
        Args:
            version: The prompt version to retrieve
            
        Returns:
            System prompt string
        """
        prompts = {
            PromptVersion.SIMPLE: FinancialAdvisorPrompts._get_simple_prompt(),
            PromptVersion.COMPLIANT: FinancialAdvisorPrompts._get_compliant_prompt(),
            PromptVersion.STRICT: FinancialAdvisorPrompts._get_strict_prompt(),
            PromptVersion.EDUCATIONAL: FinancialAdvisorPrompts._get_educational_prompt()
        }
        
        return prompts.get(version, prompts[PromptVersion.COMPLIANT])
    
    @staticmethod
    def _get_simple_prompt() -> str:
        """
        Simple financial advisor prompt - minimal compliance language.
        
        Use case: Testing basic functionality without heavy compliance overhead
        Warning: May generate non-compliant responses requiring more post-processing
        """
        return """You are a financial advisor. Provide helpful short advice about investments, finance, and money management.

Answer questions clearly and provide actionable guidance based on your knowledge.

User question: """
    
    @staticmethod
    def _get_compliant_prompt() -> str:
        """
        Compliant financial advisor prompt - balanced compliance and helpfulness.
        
        Use case: Production use with standard financial compliance requirements
        This is the current default prompt with proper disclaimers and guidelines.
        """
        return """You are a knowledgeable financial advisor providing educational information about finance and investments. 

Your responses should:
- Provide helpful, accurate financial information
- Include appropriate disclaimers and risk warnings
- Avoid guaranteeing specific returns or outcomes
- Use uncertainty language for predictions (might, could, may)
- Encourage consulting with licensed professionals for personalized advice
- Be educational rather than directive
- Include risk disclosures where appropriate

Always include a disclaimer that this is not personalized financial advice and users should consult qualified professionals for their specific situation.

User question: """
    
    @staticmethod
    def _get_strict_prompt() -> str:
        """
        Strict compliance prompt - maximum regulatory adherence.
        
        Use case: High-compliance environments or regulated financial institutions
        Emphasizes educational nature and professional consultation
        """
        return """You are an educational financial information provider. Your role is strictly educational and informational.

COMPLIANCE REQUIREMENTS:
- You are NOT a licensed financial advisor
- You do NOT provide personalized financial advice
- You do NOT make investment recommendations
- You do NOT guarantee any investment outcomes

Your responses must:
- Be purely educational and informational
- Include comprehensive risk warnings
- Use highly uncertain language (potentially, possibly, might)
- Repeatedly emphasize the need for professional consultation
- Include regulatory disclaimers
- Focus on general principles rather than specific advice

REQUIRED DISCLAIMERS:
- "This is educational information only, not financial advice"
- "Consult qualified financial professionals before making decisions"
- "Past performance does not guarantee future results"
- "All investments carry risk of loss"
- "Individual circumstances vary significantly"

Format your response to prioritize education over direction.

User question: """
    
    @staticmethod
    def _get_educational_prompt() -> str:
        """
        Educational focus prompt - emphasis on teaching financial concepts.
        
        Use case: Educational platforms, learning environments, financial literacy
        Balances compliance with strong educational value
        """
        return """You are a financial education specialist focused on teaching financial literacy and investment concepts.

Your educational approach should:
- Explain financial concepts clearly and comprehensively
- Use examples to illustrate key principles
- Break down complex topics into understandable parts
- Provide historical context and market background
- Teach both benefits and risks of different approaches
- Include relevant financial formulas or calculations when helpful
- Reference reputable financial education resources

Compliance guidelines:
- Frame advice as educational examples, not personal recommendations
- Use phrases like "generally speaking" or "typically investors might consider"
- Include appropriate disclaimers about seeking professional advice
- Emphasize the importance of personal research and due diligence
- Mention that individual circumstances greatly affect financial decisions

Educational disclaimer: "This educational content is for learning purposes. Financial decisions should be made in consultation with qualified professionals who understand your specific situation."

User question: """
    
    @staticmethod
    def get_all_prompts() -> Dict[str, str]:
        """Get all available prompts as a dictionary."""
        return {
            version.value: FinancialAdvisorPrompts.get_prompt(version)
            for version in PromptVersion
        }
    
    @staticmethod
    def compare_prompts():
        """Print a comparison of all prompt versions."""
        print("📋 FINANCIAL ADVISOR SYSTEM PROMPTS COMPARISON")
        print("=" * 60)
        
        for version in PromptVersion:
            prompt = FinancialAdvisorPrompts.get_prompt(version)
            print(f"\n🔸 {version.value.upper()} PROMPT:")
            print("-" * 40)
            print(prompt[:200] + "..." if len(prompt) > 200 else prompt)
            print(f"Length: {len(prompt)} characters")
    
    @staticmethod
    def get_prompt_characteristics() -> Dict[str, Dict[str, Any]]:
        """Get characteristics and use cases for each prompt version."""
        return {
            "simple": {
                "compliance_level": "Low",
                "response_length": "Short to Medium",
                "use_case": "Testing, development, casual use",
                "risk_level": "High - requires post-processing",
                "disclaimer_intensity": "None",
                "regulatory_suitability": "Development only"
            },
            "compliant": {
                "compliance_level": "Medium-High", 
                "response_length": "Medium",
                "use_case": "Production, general public use",
                "risk_level": "Low - built-in compliance",
                "disclaimer_intensity": "Standard",
                "regulatory_suitability": "General consumer applications"
            },
            "strict": {
                "compliance_level": "Maximum",
                "response_length": "Long",
                "use_case": "Financial institutions, regulated environments",
                "risk_level": "Minimal - over-cautious",
                "disclaimer_intensity": "Maximum",
                "regulatory_suitability": "Regulated financial services"
            },
            "educational": {
                "compliance_level": "Medium",
                "response_length": "Long",
                "use_case": "Educational platforms, financial literacy",
                "risk_level": "Low - educational focus",
                "disclaimer_intensity": "Educational",
                "regulatory_suitability": "Educational institutions"
            }
        }


# Testing functions
def test_prompts_with_sample_question():
    """Test all prompts with a sample question to see differences."""
    sample_question = "Should I invest in index funds for retirement?"
    
    print("🧪 TESTING PROMPTS WITH SAMPLE QUESTION")
    print("=" * 60)
    print(f"Sample Question: '{sample_question}'")
    print()
    
    for version in PromptVersion:
        prompt = FinancialAdvisorPrompts.get_prompt(version)
        full_prompt = prompt + sample_question
        
        print(f"🔸 {version.value.upper()} PROMPT OUTPUT:")
        print("-" * 40)
        print("Full prompt that would be sent to AI:")
        print(f"'{full_prompt[:150]}...'")
        print(f"Total length: {len(full_prompt)} characters")
        print()


def create_test_scenarios():
    """Create test scenarios for different prompt versions."""
    test_scenarios = [
        {
            "question": "What's the best stock to buy right now?",
            "expected_simple": "Direct recommendation likely",
            "expected_compliant": "General guidance with disclaimers",
            "expected_strict": "Educational information only",
            "expected_educational": "Concept explanation with examples"
        },
        {
            "question": "Can I guarantee 20% returns with this strategy?",
            "expected_simple": "May discuss guarantees directly",
            "expected_compliant": "Will soften guarantee language",
            "expected_strict": "Will strongly discourage guarantee thinking",
            "expected_educational": "Will explain why guarantees don't exist"
        },
        {
            "question": "Should I put all my money in crypto?",
            "expected_simple": "May give direct yes/no answer",
            "expected_compliant": "Balanced view with risk warnings",
            "expected_strict": "Strong educational focus on diversification",
            "expected_educational": "Comprehensive explanation of diversification principles"
        }
    ]
    
    return test_scenarios


def main():
    """Demonstrate the different prompt versions."""
    print("🏦 FINANCIAL ADVISOR PROMPTS DEMO")
    print("=" * 50)
    
    # Show prompt comparison
    FinancialAdvisorPrompts.compare_prompts()
    
    print("\n" + "=" * 60)
    print("📊 PROMPT CHARACTERISTICS")
    print("=" * 60)
    
    characteristics = FinancialAdvisorPrompts.get_prompt_characteristics()
    for version, chars in characteristics.items():
        print(f"\n🔸 {version.upper()}:")
        for key, value in chars.items():
            print(f"  • {key.replace('_', ' ').title()}: {value}")
    
    print("\n" + "=" * 60)
    
    # Test with sample question
    test_prompts_with_sample_question()
    
    print("=" * 60)
    print("💡 USAGE RECOMMENDATIONS")
    print("=" * 60)
    print("🔸 SIMPLE: Use for development/testing only")
    print("🔸 COMPLIANT: Use for production applications (default)")
    print("🔸 STRICT: Use for regulated financial institutions")
    print("🔸 EDUCATIONAL: Use for learning platforms and courses")


if __name__ == "__main__":
    main()