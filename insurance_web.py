"""
Insurance Analysis Web Module
Returns insurance analysis data in a format suitable for web display
"""

import csv
import os
from typing import Dict, Any, List


def load_insurance_data() -> Dict[str, Any]:
    """Load insurance data from CSV and return structured data for web display"""
    csv_path = os.path.join(os.path.dirname(__file__), 'insurance_analysis', 'insurance.csv')
    
    ages = []
    sexes = []
    bmis = []
    num_children = []
    smoker_statuses = []
    regions = []
    insurance_charges = []
    
    with open(csv_path, 'r') as insurance_file:
        reader = csv.DictReader(insurance_file)
        for row in reader:
            ages.append(int(row["age"]))
            sexes.append(row["sex"])
            bmis.append(float(row["bmi"]))
            num_children.append(int(row["children"]))
            smoker_statuses.append(row["smoker"])
            regions.append(row["region"])
            insurance_charges.append(float(row["charges"]))
    
    return {
        'ages': ages,
        'sexes': sexes,
        'bmis': bmis,
        'num_children': num_children,
        'smoker_statuses': smoker_statuses,
        'regions': regions,
        'insurance_charges': insurance_charges
    }


def mean(values: List[float]) -> float:
    """Calculate the mean of a list of numbers"""
    return sum(values) / len(values) if values else 0


def analyze_insurance() -> Dict[str, Any]:
    """Analyze insurance data and return insights for web display"""
    data = load_insurance_data()
    
    ages = data['ages']
    sexes = data['sexes']
    bmis = data['bmis']
    num_children = data['num_children']
    smoker_statuses = data['smoker_statuses']
    regions = data['regions']
    insurance_charges = data['insurance_charges']
    
    # Basic statistics
    total_records = len(ages)
    avg_age = round(mean(ages), 1)
    avg_bmi = round(mean(bmis), 1)
    avg_children = round(mean(num_children), 1)
    avg_charges = round(mean(insurance_charges), 2)
    
    # Smoker analysis
    smoker_charges = [c for s, c in zip(smoker_statuses, insurance_charges) if s == "yes"]
    non_smoker_charges = [c for s, c in zip(smoker_statuses, insurance_charges) if s == "no"]
    smoker_avg = round(mean(smoker_charges), 2) if smoker_charges else 0
    non_smoker_avg = round(mean(non_smoker_charges), 2) if non_smoker_charges else 0
    smoker_diff = round(smoker_avg - non_smoker_avg, 2)
    smoker_percentage = round((smoker_diff / non_smoker_avg) * 100, 1) if non_smoker_avg > 0 else 0
    
    # Region analysis
    region_data = {}
    for region, charge in zip(regions, insurance_charges):
        if region not in region_data:
            region_data[region] = []
        region_data[region].append(charge)
    
    region_stats = {}
    for region, charges in region_data.items():
        region_stats[region] = {
            'average': round(mean(charges), 2),
            'count': len(charges)
        }
    
    # Sex analysis
    male_charges = [c for s, c in zip(sexes, insurance_charges) if s == "male"]
    female_charges = [c for s, c in zip(sexes, insurance_charges) if s == "female"]
    male_avg = round(mean(male_charges), 2) if male_charges else 0
    female_avg = round(mean(female_charges), 2) if female_charges else 0
    sex_diff = round(male_avg - female_avg, 2)
    sex_percentage = round((sex_diff / female_avg) * 100, 1) if female_avg > 0 else 0
    
    # BMI category analysis
    bmi_categories = {
        'Underweight': [],
        'Normal': [],
        'Overweight': [],
        'Obese': []
    }
    
    for bmi, charge in zip(bmis, insurance_charges):
        if bmi < 18.5:
            bmi_categories['Underweight'].append(charge)
        elif bmi < 25:
            bmi_categories['Normal'].append(charge)
        elif bmi < 30:
            bmi_categories['Overweight'].append(charge)
        else:
            bmi_categories['Obese'].append(charge)
    
    bmi_stats = {}
    for category, charges in bmi_categories.items():
        if charges:
            bmi_stats[category] = {
                'average': round(mean(charges), 2),
                'count': len(charges)
            }
    
    # Age group analysis
    age_groups = {
        '18-30': [],
        '31-40': [],
        '41-50': [],
        '51-60': [],
        '60+': []
    }
    
    for age, charge in zip(ages, insurance_charges):
        if age <= 30:
            age_groups['18-30'].append(charge)
        elif age <= 40:
            age_groups['31-40'].append(charge)
        elif age <= 50:
            age_groups['41-50'].append(charge)
        elif age <= 60:
            age_groups['51-60'].append(charge)
        else:
            age_groups['60+'].append(charge)
    
    age_group_stats = {}
    for group, charges in age_groups.items():
        if charges:
            age_group_stats[group] = {
                'average': round(mean(charges), 2),
                'count': len(charges)
            }
    
    # Children analysis
    children_data = {}
    for num_kids, charge in zip(num_children, insurance_charges):
        if num_kids not in children_data:
            children_data[num_kids] = []
        children_data[num_kids].append(charge)
    
    children_stats = {}
    for num_kids in sorted(children_data.keys()):
        charges = children_data[num_kids]
        children_stats[str(num_kids)] = {
            'average': round(mean(charges), 2),
            'count': len(charges)
        }
    
    # Find highest and lowest regions
    highest_region = max(region_stats.items(), key=lambda x: x[1]['average'])
    lowest_region = min(region_stats.items(), key=lambda x: x[1]['average'])
    
    return {
        'summary': {
            'total_records': total_records,
            'average_age': avg_age,
            'average_bmi': avg_bmi,
            'average_children': avg_children,
            'average_charges': avg_charges
        },
        'smoker_analysis': {
            'smoker': {
                'average': smoker_avg,
                'count': len(smoker_charges)
            },
            'non_smoker': {
                'average': non_smoker_avg,
                'count': len(non_smoker_charges)
            },
            'difference': smoker_diff,
            'percentage_increase': smoker_percentage
        },
        'region_analysis': region_stats,
        'sex_analysis': {
            'male': {
                'average': male_avg,
                'count': len(male_charges)
            },
            'female': {
                'average': female_avg,
                'count': len(female_charges)
            },
            'difference': sex_diff,
            'percentage_increase': sex_percentage
        },
        'bmi_analysis': bmi_stats,
        'age_group_analysis': age_group_stats,
        'children_analysis': children_stats,
        'insights': {
            'highest_region': {
                'name': highest_region[0],
                'average': highest_region[1]['average']
            },
            'lowest_region': {
                'name': lowest_region[0],
                'average': lowest_region[1]['average']
            },
            'smoking_impact': smoker_percentage,
            'bmi_impact': round((bmi_stats.get('Obese', {}).get('average', 0) - 
                                bmi_stats.get('Normal', {}).get('average', 0)) / 
                               bmi_stats.get('Normal', {}).get('average', 1) * 100, 1) 
                           if bmi_stats.get('Normal', {}).get('average', 0) > 0 else 0
        }
    }

