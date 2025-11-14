"""
Student Data Analysis Module
Analyzes student performance data with statistical visualizations
"""

from typing import Dict, Any, List
import random


def generate_sample_student_data() -> List[Dict[str, Any]]:
    """Generate sample student data for demonstration"""
    jobs = ['teacher', 'health', 'services', 'at_home', 'other']
    addresses = ['U', 'R']  # Urban, Rural
    
    students = []
    for i in range(100):
        students.append({
            'math_grade': random.randint(0, 20),
            'absences': random.randint(0, 30),
            'Mjob': random.choice(jobs),
            'Fjob': random.choice(jobs),
            'address': random.choice(addresses)
        })
    return students


def analyze_students() -> Dict[str, Any]:
    """Main analysis function for student data"""
    students = generate_sample_student_data()
    
    # Extract data
    math_grades = [s['math_grade'] for s in students]
    absences = [s['absences'] for s in students]
    
    # Calculate statistics
    mean_grade = sum(math_grades) / len(math_grades)
    sorted_grades = sorted(math_grades)
    n = len(sorted_grades)
    median_grade = (sorted_grades[n//2] + sorted_grades[(n-1)//2]) / 2 if n % 2 == 0 else sorted_grades[n//2]
    
    # Mode
    grade_counts = {}
    for grade in math_grades:
        grade_counts[grade] = grade_counts.get(grade, 0) + 1
    mode_grade = max(grade_counts, key=grade_counts.get)
    
    # Range and standard deviation
    grade_range = max(math_grades) - min(math_grades)
    variance = sum((x - mean_grade) ** 2 for x in math_grades) / len(math_grades)
    std_grade = variance ** 0.5
    
    # Mean absolute deviation
    mad_grade = sum(abs(x - mean_grade) for x in math_grades) / len(math_grades)
    
    # Job distributions
    mjob_counts = {}
    fjob_counts = {}
    for s in students:
        mjob_counts[s['Mjob']] = mjob_counts.get(s['Mjob'], 0) + 1
        fjob_counts[s['Fjob']] = fjob_counts.get(s['Fjob'], 0) + 1
    
    # Address distribution
    address_counts = {}
    for s in students:
        address_counts[s['address']] = address_counts.get(s['address'], 0) + 1
    
    # Grade distribution for histogram
    grade_bins = {}
    for grade in math_grades:
        bin_key = (grade // 2) * 2  # Group into bins of 2
        grade_bins[bin_key] = grade_bins.get(bin_key, 0) + 1
    
    return {
        'summary': {
            'total_students': len(students),
            'mean_grade': round(mean_grade, 2),
            'median_grade': round(median_grade, 2),
            'mode_grade': mode_grade,
            'grade_range': grade_range,
            'std_grade': round(std_grade, 2),
            'mad_grade': round(mad_grade, 2)
        },
        'grade_distribution': dict(sorted(grade_bins.items())),
        'mjob_distribution': mjob_counts,
        'fjob_distribution': fjob_counts,
        'address_distribution': address_counts,
        'absences_summary': {
            'mean': round(sum(absences) / len(absences), 2),
            'max': max(absences),
            'min': min(absences),
            'median': sorted(absences)[len(absences)//2]
        },
        'grade_bins': list(range(0, 21, 2))
    }

