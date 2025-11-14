"""
Medical System Module
Manages and analyzes patient medical records
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime

def load_medical_data() -> Dict[str, Any]:
    """Load medical records from JSON file"""
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'medical_records.json')
    with open(data_path, 'r') as f:
        return json.load(f)

def analyze_medical_records() -> Dict[str, Any]:
    """Analyze medical records and return insights"""
    data = load_medical_data()
    patients = data.get('patients', [])
    
    if not patients:
        return {"error": "No medical records available"}
    
    # Calculate statistics
    total_patients = len(patients)
    avg_age = sum(p.get('age', 0) for p in patients) / total_patients if patients else 0
    
    # Diagnosis distribution
    diagnosis_dist = {}
    for p in patients:
        diag = p.get('diagnosis', 'Unknown')
        diagnosis_dist[diag] = diagnosis_dist.get(diag, 0) + 1
    
    # Medication analysis
    all_medications = []
    for p in patients:
        all_medications.extend(p.get('medications', []))
    medication_counts = {}
    for med in all_medications:
        medication_counts[med] = medication_counts.get(med, 0) + 1
    
    # Vital signs analysis
    blood_pressures = []
    heart_rates = []
    temperatures = []
    
    for p in patients:
        vs = p.get('vital_signs', {})
        bp = vs.get('blood_pressure', '')
        if bp:
            # Extract systolic (first number)
            try:
                systolic = int(bp.split('/')[0])
                blood_pressures.append(systolic)
            except:
                pass
        
        hr = vs.get('heart_rate', 0)
        if hr:
            heart_rates.append(hr)
        
        temp = vs.get('temperature', 0)
        if temp:
            temperatures.append(temp)
    
    # Age groups
    age_groups = {
        "18-30": 0,
        "31-45": 0,
        "46-60": 0,
        "60+": 0
    }
    
    for p in patients:
        age = p.get('age', 0)
        if 18 <= age <= 30:
            age_groups["18-30"] += 1
        elif 31 <= age <= 45:
            age_groups["31-45"] += 1
        elif 46 <= age <= 60:
            age_groups["46-60"] += 1
        elif age > 60:
            age_groups["60+"] += 1
    
    return {
        "summary": {
            "total_patients": total_patients,
            "average_age": round(avg_age, 1)
        },
        "diagnosis_distribution": diagnosis_dist,
        "medication_usage": medication_counts,
        "vital_signs_stats": {
            "average_systolic_bp": round(sum(blood_pressures) / len(blood_pressures), 1) if blood_pressures else 0,
            "average_heart_rate": round(sum(heart_rates) / len(heart_rates), 1) if heart_rates else 0,
            "average_temperature": round(sum(temperatures) / len(temperatures), 2) if temperatures else 0
        },
        "age_distribution": age_groups,
        "all_patients": patients
    }

def main():
    """Main function for command-line use"""
    results = analyze_medical_records()
    print("\n=== Medical Records Analysis ===")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
