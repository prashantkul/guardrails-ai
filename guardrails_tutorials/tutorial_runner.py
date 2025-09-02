#!/usr/bin/env python3
"""
Guardrails AI Tutorials - Main Runner
======================================

Interactive tutorial system for learning to implement various guardrails.

Usage:
    python tutorial_runner.py [--tutorial N] [--solution]
"""

import sys
import argparse
import importlib.util
from pathlib import Path
from typing import Dict, Any


class TutorialRunner:
    """Main tutorial runner for the Guardrails AI tutorial system."""
    
    def __init__(self):
        self.tutorials = {
            1: {
                "title": "Ban List Guardrail",
                "description": "Learn to implement content filtering using banned words/phrases",
                "difficulty": "⭐☆☆ (Beginner)",
                "file": "01_ban_list.py",
                "concepts": ["Pattern matching", "Case sensitivity", "Word boundaries"]
            },
            2: {
                "title": "Valid JSON Guardrail", 
                "description": "Validate and fix JSON format in AI outputs",
                "difficulty": "⭐⭐☆ (Intermediate)",
                "file": "02_valid_json.py",
                "concepts": ["JSON parsing", "Error handling", "Format fixing"]
            },
            3: {
                "title": "Logic Check Guardrail",
                "description": "Detect logical inconsistencies and contradictions",
                "difficulty": "⭐⭐⭐ (Advanced)",
                "file": "03_logic_check.py", 
                "concepts": ["Contradiction detection", "Math validation", "Causality checking"]
            },
            4: {
                "title": "Saliency Check Guardrail",
                "description": "Ensure content focuses on important/relevant topics",
                "difficulty": "⭐⭐⭐ (Advanced)",
                "file": "04_saliency_check.py",
                "concepts": ["Keyword importance", "Content focus", "Relevance scoring"]
            },
            5: {
                "title": "Restrict to Topic Guardrail",
                "description": "Keep AI responses within specified topic boundaries",
                "difficulty": "⭐⭐☆ (Intermediate)", 
                "file": "05_restrict_to_topic.py",
                "concepts": ["Topic classification", "Keyword matching", "LLM integration"]
            },
            6: {
                "title": "Exclude SQL Predicates Guardrail",
                "description": "Prevent SQL injection attempts and malicious queries",
                "difficulty": "⭐⭐☆ (Intermediate)",
                "file": "06_exclude_sql_predicates.py",
                "concepts": ["SQL injection patterns", "Security validation", "Syntax analysis"]
            },
            7: {
                "title": "Grounded AI Hallucination Detection",
                "description": "Detect AI hallucinations using grounding techniques",
                "difficulty": "⭐⭐⭐ (Advanced)",
                "file": "07_grounded_ai_hallucination.py",
                "concepts": ["Fact checking", "Uncertainty analysis", "Knowledge base verification"]
            }
        }
    
    def show_menu(self):
        """Display the main tutorial menu."""
        print("=" * 80)
        print("🛡️  GUARDRAILS AI TUTORIALS")
        print("=" * 80)
        print("Learn to implement various AI safety guardrails step-by-step!")
        print("\nAvailable Tutorials:")
        print("-" * 80)
        
        for num, tutorial in self.tutorials.items():
            print(f"\n{num}. {tutorial['title']} {tutorial['difficulty']}")
            print(f"   📝 {tutorial['description']}")
            print(f"   🎯 Key concepts: {', '.join(tutorial['concepts'])}")
        
        print("\n" + "=" * 80)
        print("💡 Tips:")
        print("   • Start with tutorial 1 if you're new to guardrails")
        print("   • Each tutorial has TODO sections for you to complete")
        print("   • Solutions are available in the solutions/ folder")
        print("   • Run tests to verify your implementation")
        
        print("\n🚀 Usage:")
        print("   python tutorial_runner.py --tutorial 1    # Run tutorial 1")
        print("   python tutorial_runner.py --solution 1    # Show solution for tutorial 1")
        print("   python tutorial_runner.py --list          # Show this menu")
    
    def run_tutorial(self, tutorial_num: int, show_solution: bool = False):
        """Run a specific tutorial."""
        if tutorial_num not in self.tutorials:
            print(f"❌ Tutorial {tutorial_num} not found!")
            print(f"Available tutorials: {list(self.tutorials.keys())}")
            return
        
        tutorial = self.tutorials[tutorial_num]
        folder = "solutions" if show_solution else "exercises"
        
        if show_solution:
            filename = tutorial['file'].replace('.py', '_solution.py')
        else:
            filename = tutorial['file']
        
        file_path = Path(__file__).parent / folder / filename
        
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return
        
        print("=" * 80)
        if show_solution:
            print(f"🔍 SOLUTION: {tutorial['title']}")
        else:
            print(f"🎓 TUTORIAL {tutorial_num}: {tutorial['title']}")
        print("=" * 80)
        print(f"📖 Description: {tutorial['description']}")
        print(f"📊 Difficulty: {tutorial['difficulty']}")
        print(f"🎯 Concepts: {', '.join(tutorial['concepts'])}")
        print("-" * 80)
        
        if not show_solution:
            print("📋 Instructions:")
            print("1. Open the tutorial file in your editor")
            print("2. Complete all TODO sections")
            print("3. Run the file to test your implementation")
            print("4. Check the solution if you get stuck")
            print()
            print(f"📂 File location: {file_path}")
            print(f"🔍 Solution: python tutorial_runner.py --solution {tutorial_num}")
        else:
            print("✅ This is the complete solution for reference.")
            print("📚 Study the implementation to understand the concepts.")
        
        print("\n" + "=" * 80)
        
        # Ask if user wants to run the tutorial
        try:
            if show_solution:
                response = input(f"📄 Do you want to view the solution code? (y/N): ").strip().lower()
            else:
                response = input(f"🚀 Do you want to run the tutorial now? (y/N): ").strip().lower()
            
            if response in ['y', 'yes']:
                print("\n🔄 Running tutorial...")
                self._execute_tutorial(file_path)
        except KeyboardInterrupt:
            print("\n\n⏹️  Cancelled by user")
    
    def _execute_tutorial(self, file_path: Path):
        """Execute a tutorial file."""
        try:
            # Import and run the tutorial module
            spec = importlib.util.spec_from_file_location("tutorial", file_path)
            tutorial_module = importlib.util.module_from_spec(spec)
            
            print("-" * 80)
            
            # Execute the tutorial
            spec.loader.exec_module(tutorial_module)
            
        except Exception as e:
            print(f"❌ Error running tutorial: {e}")
            print("\n💡 This might happen if you haven't completed the TODO sections yet.")
            print("📝 Please implement the required methods and try again.")
    
    def show_progress(self):
        """Show tutorial completion progress."""
        print("=" * 80)
        print("📈 TUTORIAL PROGRESS")
        print("=" * 80)
        
        exercises_dir = Path(__file__).parent / "exercises"
        solutions_dir = Path(__file__).parent / "solutions"
        
        for num, tutorial in self.tutorials.items():
            exercise_file = exercises_dir / tutorial['file']
            solution_file = solutions_dir / tutorial['file'].replace('.py', '_solution.py')
            
            exercise_exists = exercise_file.exists()
            solution_exists = solution_file.exists()
            
            status = "✅" if exercise_exists and solution_exists else "🚧"
            
            print(f"{status} Tutorial {num}: {tutorial['title']}")
            print(f"   📂 Exercise: {'✅' if exercise_exists else '❌'}")
            print(f"   🔍 Solution: {'✅' if solution_exists else '❌'}")
        
        print("\n" + "=" * 80)


def main():
    """Main entry point for the tutorial runner."""
    parser = argparse.ArgumentParser(
        description="Guardrails AI Tutorials - Interactive Learning System"
    )
    parser.add_argument("--tutorial", "-t", type=int, metavar="N",
                       help="Run tutorial N (1-7)")
    parser.add_argument("--solution", "-s", type=int, metavar="N", 
                       help="Show solution for tutorial N")
    parser.add_argument("--list", "-l", action="store_true",
                       help="Show available tutorials")
    parser.add_argument("--progress", "-p", action="store_true",
                       help="Show completion progress")
    
    args = parser.parse_args()
    
    runner = TutorialRunner()
    
    if args.tutorial:
        runner.run_tutorial(args.tutorial, show_solution=False)
    elif args.solution:
        runner.run_tutorial(args.solution, show_solution=True)
    elif args.list:
        runner.show_menu()
    elif args.progress:
        runner.show_progress()
    else:
        runner.show_menu()


if __name__ == "__main__":
    main()