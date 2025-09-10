#!/usr/bin/env python3
"""
SpaCy Financial Risk NER
========================

Custom Named Entity Recognition for financial risk detection using spaCy
with rule-based patterns and custom entity labels.
"""

import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass


@dataclass
class FinancialRiskEntity:
    """Represents a detected financial risk entity."""
    text: str
    label: str
    start: int
    end: int
    risk_level: str
    description: str


class FinancialRiskNER:
    """
    Custom spaCy NER for detecting financial risk entities.
    """
    
    def __init__(self):
        # Load English model
        self.nlp = spacy.load("en_core_web_sm")
        
        # Initialize matcher for pattern-based entity recognition
        self.matcher = Matcher(self.nlp.vocab)
        
        # Define custom financial risk entity labels
        self.risk_labels = {
            'GUARANTEE_LANG': {'level': 'high', 'desc': 'Guaranteed return language'},
            'RISK_FREE_CLAIM': {'level': 'high', 'desc': 'Risk-free investment claims'},
            'CERTAINTY_LANG': {'level': 'medium', 'desc': 'Overly certain predictions'},
            'GET_RICH_QUICK': {'level': 'medium', 'desc': 'Get-rich-quick schemes'},
            'INSIDER_INFO': {'level': 'high', 'desc': 'Insider trading references'},
            'NO_LOSS_CLAIM': {'level': 'high', 'desc': 'Cannot lose promises'},
            'SPECIFIC_PREDICT': {'level': 'medium', 'desc': 'Specific price/time predictions'},
            'PRESSURE_TACTIC': {'level': 'low', 'desc': 'High-pressure sales tactics'},
            'UNREALISTIC_RETURN': {'level': 'high', 'desc': 'Unrealistic return claims'}
        }
        
        # Get or create entity ruler (it may already exist)
        if "entity_ruler" not in self.nlp.pipe_names:
            self.entity_ruler = self.nlp.add_pipe("entity_ruler", before="ner")
        else:
            self.entity_ruler = self.nlp.get_pipe("entity_ruler")
        
        # Register patterns
        self._register_patterns()
    
    def _register_patterns(self):
        """Register spaCy patterns for financial risk detection."""
        
        # Guarantee language patterns
        guarantee_patterns = [
            [{"LOWER": "guarantee"}, {"IS_ALPHA": True, "OP": "*"}, {"LOWER": {"IN": ["profit", "return", "money", "gains", "income"]}}],
            [{"LOWER": "guaranteed"}, {"LOWER": {"IN": ["returns", "profits", "money", "gains"]}}],
            [{"LOWER": "assured"}, {"IS_ALPHA": True, "OP": "*"}, {"LOWER": {"IN": ["profit", "return", "success"]}}],
            [{"LOWER": "certain"}, {"IS_ALPHA": True, "OP": "*"}, {"LOWER": {"IN": ["profit", "return", "money"]}}],
            [{"TEXT": {"REGEX": r"100%"}}, {"LOWER": {"IN": ["safe", "secure", "guaranteed", "certain"]}}]
        ]
        
        # Risk-free claim patterns
        risk_free_patterns = [
            [{"LOWER": {"REGEX": r"risk[-\s]?free"}}],
            [{"LOWER": "no"}, {"LOWER": {"REGEX": r"risk"}}],
            [{"LOWER": "zero"}, {"LOWER": "risk"}],
            [{"LOWER": "completely"}, {"LOWER": "safe"}],
            [{"LOWER": "totally"}, {"LOWER": "safe"}]
        ]
        
        # Certainty language patterns
        certainty_patterns = [
            [{"LOWER": "will"}, {"LOWER": {"IN": ["definitely", "certainly", "surely"]}}],
            [{"LOWER": {"IN": ["definitely", "certainly"]}}, {"LOWER": "will"}],
            [{"LOWER": "without"}, {"LOWER": {"IN": ["doubt", "question"]}}],
            [{"LOWER": {"REGEX": r"can['']?t"}}, {"LOWER": {"IN": ["fail", "lose"]}}],
            [{"LOWER": "impossible"}, {"LOWER": "to"}, {"LOWER": {"IN": ["lose", "fail"]}}]
        ]
        
        # Get rich quick patterns
        get_rich_patterns = [
            [{"LOWER": {"IN": ["quick", "fast", "easy"]}}, {"LOWER": {"IN": ["money", "profit", "cash", "rich"]}}],
            [{"LOWER": "overnight"}, {"LOWER": {"IN": ["success", "millionaire", "rich"]}}],
            [{"LOWER": "instant"}, {"LOWER": {"IN": ["wealth", "riches", "money"]}}],
            [{"LOWER": "make"}, {"LOWER": {"REGEX": r"millions?"}}, {"LOWER": {"IN": ["quickly", "fast"]}}]
        ]
        
        # Insider information patterns
        insider_patterns = [
            [{"LOWER": {"IN": ["secret", "hidden", "insider"]}}, {"LOWER": {"IN": ["tip", "tips", "information", "knowledge"]}}],
            [{"LOWER": "exclusive"}, {"LOWER": {"IN": ["access", "information", "secret"]}}],
            [{"LOWER": "confidential"}, {"LOWER": {"IN": ["tip", "strategy", "method"]}}],
            [{"LOWER": "nobody"}, {"LOWER": "knows"}, {"LOWER": "about"}]
        ]
        
        # Cannot lose patterns
        no_loss_patterns = [
            [{"LOWER": "cannot"}, {"LOWER": {"IN": ["lose", "fail"]}}],
            [{"LOWER": {"REGEX": r"can['']?t"}}, {"LOWER": {"IN": ["lose", "fail"]}}],
            [{"LOWER": "no"}, {"LOWER": "chance"}, {"LOWER": "of"}, {"LOWER": {"IN": ["loss", "losing"]}}],
            [{"LOWER": "impossible"}, {"LOWER": "to"}, {"LOWER": "lose"}]
        ]
        
        # Specific prediction patterns
        prediction_patterns = [
            [{"LOWER": "will"}, {"LOWER": "hit"}, {"TEXT": {"REGEX": r"\$[\d,]+"}}],
            [{"LOWER": "by"}, {"LOWER": {"IN": ["next", "tomorrow"]}}, {"LOWER": {"IN": ["week", "month", "year"]}, "OP": "?"}],
            [{"LOWER": "exactly"}, {"TEXT": {"REGEX": r"\d+%"}}, {"LOWER": {"IN": ["gain", "return"]}}],
            [{"LOWER": "going"}, {"LOWER": "to"}, {"TEXT": {"REGEX": r"\$[\d,]+"}}]
        ]
        
        # Pressure tactic patterns
        pressure_patterns = [
            [{"LOWER": {"IN": ["act", "buy", "invest"]}}, {"LOWER": {"IN": ["now", "immediately", "today"]}}],
            [{"LOWER": "limited"}, {"LOWER": {"IN": ["time", "offer", "opportunity"]}}],
            [{"LOWER": {"REGEX": r"don['']?t"}}, {"LOWER": {"IN": ["wait", "delay", "miss"]}}],
            [{"LOWER": "once"}, {"LOWER": "in"}, {"LOWER": "a"}, {"LOWER": "lifetime"}]
        ]
        
        # Unrealistic return patterns
        unrealistic_patterns = [
            [{"TEXT": {"REGEX": r"[5-9]\d{2,}%"}}, {"LOWER": {"IN": ["return", "profit", "gain"]}}],
            [{"TEXT": {"REGEX": r"(1000|2000|5000)%"}}, {"LOWER": {"IN": ["return", "gain"]}}],
            [{"LOWER": {"REGEX": r"millions?"}}, {"LOWER": "in"}, {"LOWER": {"IN": ["days", "weeks", "months"]}}],
            [{"LOWER": "double"}, {"LOWER": "your"}, {"LOWER": "money"}, {"LOWER": "in"}, {"LOWER": {"IN": ["days", "weeks"]}}]
        ]
        
        # Register all patterns with their labels
        pattern_groups = [
            ("GUARANTEE_LANG", guarantee_patterns),
            ("RISK_FREE_CLAIM", risk_free_patterns),
            ("CERTAINTY_LANG", certainty_patterns),
            ("GET_RICH_QUICK", get_rich_patterns),
            ("INSIDER_INFO", insider_patterns),
            ("NO_LOSS_CLAIM", no_loss_patterns),
            ("SPECIFIC_PREDICT", prediction_patterns),
            ("PRESSURE_TACTIC", pressure_patterns),
            ("UNREALISTIC_RETURN", unrealistic_patterns)
        ]
        
        # Add patterns to entity ruler
        for label, patterns in pattern_groups:
            for pattern in patterns:
                pattern_dict = {"label": label, "pattern": pattern}
                self.entity_ruler.add_patterns([pattern_dict])
    
    def analyze_text(self, text: str) -> Tuple[List[FinancialRiskEntity], Dict[str, Any]]:
        """
        Analyze text for financial risk entities.
        
        Args:
            text: Text to analyze
            
        Returns:
            Tuple of (entities_list, analysis_summary)
        """
        doc = self.nlp(text)
        
        entities = []
        risk_counts = {'high': 0, 'medium': 0, 'low': 0}
        
        # Process NER entities
        for ent in doc.ents:
            # Only process our custom financial risk labels
            if ent.label_ in self.risk_labels:
                risk_info = self.risk_labels[ent.label_]
                
                entity = FinancialRiskEntity(
                    text=ent.text,
                    label=ent.label_,
                    start=ent.start_char,
                    end=ent.end_char,
                    risk_level=risk_info['level'],
                    description=risk_info['desc']
                )
                
                entities.append(entity)
                risk_counts[risk_info['level']] += 1
        
        # Calculate overall risk assessment
        overall_risk = 'low'
        if risk_counts['high'] > 0:
            overall_risk = 'high'
        elif risk_counts['medium'] > 1 or (risk_counts['medium'] > 0 and risk_counts['low'] > 0):
            overall_risk = 'medium'
        
        analysis_summary = {
            'overall_risk': overall_risk,
            'total_entities': len(entities),
            'risk_breakdown': risk_counts,
            'confidence': min(0.95, len(entities) * 0.2 + 0.3)  # Simple confidence calculation
        }
        
        return entities, analysis_summary
    
    def get_violations_summary(self, entities: List[FinancialRiskEntity]) -> str:
        """Generate human-readable violations summary."""
        if not entities:
            return "No financial risk violations detected"
        
        violations_by_level = {'high': [], 'medium': [], 'low': []}
        for entity in entities:
            violations_by_level[entity.risk_level].append(entity.description)
        
        summary_parts = []
        for level in ['high', 'medium', 'low']:
            if violations_by_level[level]:
                unique_violations = list(set(violations_by_level[level]))
                level_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}[level]
                summary_parts.append(f"{level_emoji} {level.upper()}: {', '.join(unique_violations)}")
        
        return "; ".join(summary_parts)


def test_spacy_financial_ner():
    """Test the spaCy Financial Risk NER system."""
    print("🧪 TESTING SPACY FINANCIAL RISK NER")
    print("=" * 60)
    
    ner = FinancialRiskNER()
    
    test_cases = [
        # High risk cases
        "What's a guaranteed risk-free way to make quick money with secret insider tips?",
        "I guarantee 100% returns with zero risk - cannot lose!",
        "This strategy will definitely make you millions overnight",
        
        # Medium risk cases
        "This stock will hit $500 by next week definitely",
        "Best investment that typically works well",
        "You should act now for good returns",
        
        # Low risk cases
        "Investments may potentially provide returns over time",
        "Consider diversifying your portfolio with professional advice", 
        "Past performance does not guarantee future results",
        
        # Clean cases
        "Can you explain how compound interest works?",
        "What are some general investment principles?",
    ]
    
    print(f"Testing {len(test_cases)} financial statements:\n")
    
    for i, text in enumerate(test_cases, 1):
        print(f"📝 **Test {i}**: '{text}'")
        
        entities, summary = ner.analyze_text(text)
        
        print(f"   🎯 Overall Risk: {summary['overall_risk'].upper()}")
        print(f"   📊 Entities Found: {summary['total_entities']}")
        print(f"   🎯 Confidence: {summary['confidence']:.2%}")
        
        if entities:
            print(f"   🚨 Risk Entities:")
            for entity in entities[:3]:  # Show first 3
                print(f"      • '{entity.text}' → {entity.description} ({entity.risk_level})")
        
        violations = ner.get_violations_summary(entities)
        print(f"   📋 Summary: {violations}")
        print()


def main():
    """Run spaCy Financial Risk NER tests."""
    print("🧪 SPACY FINANCIAL RISK NER SYSTEM")
    print("=" * 70)
    print("Custom Named Entity Recognition for financial compliance")
    print()
    
    try:
        test_spacy_financial_ner()
        
        print("=" * 70)
        print("🎉 SPACY NER TESTING COMPLETE!")
        print("=" * 70)
        
        print("\n✅ **SpaCy NER Advantages:**")
        print("   • Linguistic context awareness (understands word relationships)")
        print("   • Flexible pattern matching with linguistic features")
        print("   • Token-level analysis (better than regex for complex phrases)")
        print("   • Extensible with custom patterns and rules")
        print("   • Entity boundaries detection (exact phrase extraction)")
        
        print("\n🚀 **Integration Benefits:**")
        print("   • Can complement existing guardrails validator")
        print("   • Provides detailed entity-level analysis")
        print("   • Better handling of complex linguistic patterns")
        print("   • Structured risk entity extraction")
        
        print("\n💡 **Perfect For:**")
        print("   • Enhanced prompt violation analysis")
        print("   • Detailed compliance entity highlighting")
        print("   • Linguistic pattern-based risk detection")
        print("   • Professional NLP-powered compliance checking")
        
    except Exception as e:
        print(f"\n❌ SPACY NER TESTS FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()