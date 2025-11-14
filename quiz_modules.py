"""
Quiz Modules
Interactive quiz system with multiple question types
"""

import json
import random
from typing import Dict, List, Any

def get_quiz_questions() -> List[Dict[str, Any]]:
    """Get quiz questions"""
    return [
        {
            "id": 1,
            "question": "What is the capital of France?",
            "options": ["London", "Berlin", "Paris", "Madrid"],
            "correct": 2,
            "category": "Geography"
        },
        {
            "id": 2,
            "question": "What is 15 * 7?",
            "options": ["100", "105", "110", "115"],
            "correct": 1,
            "category": "Math"
        },
        {
            "id": 3,
            "question": "Which planet is known as the Red Planet?",
            "options": ["Venus", "Mars", "Jupiter", "Saturn"],
            "correct": 1,
            "category": "Science"
        },
        {
            "id": 4,
            "question": "What is the largest ocean on Earth?",
            "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
            "correct": 3,
            "category": "Geography"
        },
        {
            "id": 5,
            "question": "Who wrote 'Romeo and Juliet'?",
            "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
            "correct": 1,
            "category": "Literature"
        },
        {
            "id": 6,
            "question": "What is the chemical symbol for Gold?",
            "options": ["Go", "Gd", "Au", "Ag"],
            "correct": 2,
            "category": "Science"
        },
        {
            "id": 7,
            "question": "What is the square root of 64?",
            "options": ["6", "7", "8", "9"],
            "correct": 2,
            "category": "Math"
        },
        {
            "id": 8,
            "question": "In which year did World War II end?",
            "options": ["1943", "1944", "1945", "1946"],
            "correct": 2,
            "category": "History"
        }
    ]

def analyze_quiz_data() -> Dict[str, Any]:
    """Analyze quiz questions and return insights"""
    questions = get_quiz_questions()
    
    # Category distribution
    category_dist = {}
    for q in questions:
        cat = q.get('category', 'Unknown')
        category_dist[cat] = category_dist.get(cat, 0) + 1
    
    # Difficulty analysis (based on question type)
    difficulty_dist = {
        "Easy": len([q for q in questions if q.get('category') in ['Geography', 'Literature']]),
        "Medium": len([q for q in questions if q.get('category') in ['Math', 'History']]),
        "Hard": len([q for q in questions if q.get('category') in ['Science']])
    }
    
    return {
        "summary": {
            "total_questions": len(questions),
            "categories_covered": len(category_dist)
        },
        "category_distribution": category_dist,
        "difficulty_distribution": difficulty_dist,
        "all_questions": questions
    }

def main():
    """Main function for command-line use"""
    results = analyze_quiz_data()
    print("\n=== Quiz Module Analysis ===")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
