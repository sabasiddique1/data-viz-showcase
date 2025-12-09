"""
A/B Testing Analysis - Farmburg's A/B Test
Analyzes click-through and conversion rates for A/B test
"""

import pandas as pd
import numpy as np
import json
import os
from scipy.stats import chi2_contingency

def load_ab_test_data():
    """Load A/B test data"""
    try:
        csv_path = os.path.join('csv', 'clicks.csv')
        if os.path.exists(csv_path):
            return pd.read_csv(csv_path)
        else:
            return generate_sample_ab_test_data()
    except Exception as e:
        print(f"Error loading A/B test data: {e}")
        return generate_sample_ab_test_data()

def generate_sample_ab_test_data():
    """Generate sample A/B test data"""
    np.random.seed(42)
    
    n_samples = 5000
    groups = ['A', 'B']
    
    data = {
        'user_id': [f'user_{i}' for i in range(n_samples)],
        'group': np.random.choice(groups, n_samples),
        'is_purchase': np.random.choice(['Yes', 'No'], n_samples, p=[0.15, 0.85])
    }
    
    return pd.DataFrame(data)

def analyze_ab_test():
    """Analyze A/B test data and return results for visualization"""
    abdata = load_ab_test_data()
    
    # Convert is_purchase to binary
    abdata['purchased'] = (abdata['is_purchase'] == 'Yes').astype(int)
    
    # Overall statistics
    total_users = len(abdata)
    total_purchases = abdata['purchased'].sum()
    overall_conversion_rate = (total_purchases / total_users) * 100
    
    # Group A statistics
    group_a = abdata[abdata['group'] == 'A']
    group_a_users = len(group_a)
    group_a_purchases = group_a['purchased'].sum()
    group_a_conversion = (group_a_purchases / group_a_users) * 100 if group_a_users > 0 else 0
    
    # Group B statistics
    group_b = abdata[abdata['group'] == 'B']
    group_b_users = len(group_b)
    group_b_purchases = group_b['purchased'].sum()
    group_b_conversion = (group_b_purchases / group_b_users) * 100 if group_b_users > 0 else 0
    
    # Conversion rate difference
    conversion_diff = group_b_conversion - group_a_conversion
    relative_lift = (conversion_diff / group_a_conversion * 100) if group_a_conversion > 0 else 0
    
    # Chi-square test
    contingency = pd.crosstab(abdata['group'], abdata['is_purchase'])
    chi2, pval, dof, expected = chi2_contingency(contingency.values)
    
    # Statistical significance (convert numpy bool to Python bool for JSON serialization)
    is_significant = bool(pval < 0.05)
    
    # Sample size analysis
    sample_size_a = group_a_users
    sample_size_b = group_b_users
    
    results = {
        'overall_stats': {
            'total_users': int(total_users),
            'total_purchases': int(total_purchases),
            'overall_conversion_rate': round(float(overall_conversion_rate), 2)
        },
        'group_a': {
            'users': int(group_a_users),
            'purchases': int(group_a_purchases),
            'conversion_rate': round(float(group_a_conversion), 2)
        },
        'group_b': {
            'users': int(group_b_users),
            'purchases': int(group_b_purchases),
            'conversion_rate': round(float(group_b_conversion), 2)
        },
        'comparison': {
            'conversion_difference': round(float(conversion_diff), 2),
            'relative_lift_percent': round(float(relative_lift), 2),
            'is_significant': bool(is_significant)  # Explicitly convert to bool
        },
        'statistical_test': {
            'chi2': round(float(chi2), 4),
            'p_value': round(float(pval), 6),
            'degrees_of_freedom': int(dof),
            'significant': bool(is_significant)  # Explicitly convert to bool
        },
        'contingency_table': {
            'group_a': {
                'yes': int(contingency.loc['A', 'Yes']) if 'A' in contingency.index and 'Yes' in contingency.columns else 0,
                'no': int(contingency.loc['A', 'No']) if 'A' in contingency.index and 'No' in contingency.columns else 0
            },
            'group_b': {
                'yes': int(contingency.loc['B', 'Yes']) if 'B' in contingency.index and 'Yes' in contingency.columns else 0,
                'no': int(contingency.loc['B', 'No']) if 'B' in contingency.index and 'No' in contingency.columns else 0
            }
        }
    }
    
    return results

if __name__ == '__main__':
    results = analyze_ab_test()
    print(json.dumps(results, indent=2))

