"""
Familiar Data Analysis
Analyzes lifespan and iron levels in different packs
"""

import pandas as pd
import numpy as np
import json
import os
from scipy.stats import ttest_ind, chi2_contingency

def load_familiar_data():
    """Load familiar data"""
    try:
        lifespan_path = os.path.join('csv', 'familiar_lifespan.csv')
        iron_path = os.path.join('csv', 'familiar_iron.csv')
        
        if os.path.exists(lifespan_path) and os.path.exists(iron_path):
            lifespans = pd.read_csv(lifespan_path)
            iron = pd.read_csv(iron_path)
            return lifespans, iron
        else:
            return generate_sample_familiar_data()
    except Exception as e:
        print(f"Error loading familiar data: {e}")
        return generate_sample_familiar_data()

def generate_sample_familiar_data():
    """Generate sample familiar data"""
    np.random.seed(42)
    
    packs = ['vein', 'artery']
    n_samples = 100
    
    lifespans = pd.DataFrame({
        'pack': np.random.choice(packs, n_samples),
        'lifespan': np.random.normal(75, 2, n_samples)
    })
    
    iron_levels = ['low', 'normal', 'high']
    iron = pd.DataFrame({
        'pack': np.random.choice(packs, n_samples * 3),
        'iron': np.random.choice(iron_levels, n_samples * 3, p=[0.2, 0.6, 0.2])
    })
    
    return lifespans, iron

def analyze_familiar():
    """Analyze familiar data and return results for visualization"""
    lifespans, iron = load_familiar_data()
    
    # Lifespan analysis by pack
    lifespan_by_pack = lifespans.groupby('pack')['lifespan'].agg(['mean', 'std', 'count']).to_dict()
    
    # Statistical test for lifespan difference
    vein_lifespan = lifespans[lifespans['pack'] == 'vein']['lifespan']
    artery_lifespan = lifespans[lifespans['pack'] == 'artery']['lifespan']
    
    tstat, pval = ttest_ind(vein_lifespan, artery_lifespan)
    
    # Iron level distribution
    iron_distribution = iron.groupby(['pack', 'iron']).size().unstack(fill_value=0)
    
    # Chi-square test for iron levels
    contingency = iron_distribution.values
    chi2, pval_iron, dof, expected = chi2_contingency(contingency)
    
    results = {
        'lifespan_stats': {
            'vein': {
                'mean': float(lifespan_by_pack['mean'].get('vein', 0)),
                'std': float(lifespan_by_pack['std'].get('vein', 0)),
                'count': int(lifespan_by_pack['count'].get('vein', 0))
            },
            'artery': {
                'mean': float(lifespan_by_pack['mean'].get('artery', 0)),
                'std': float(lifespan_by_pack['std'].get('artery', 0)),
                'count': int(lifespan_by_pack['count'].get('artery', 0))
            }
        },
        'lifespan_test': {
            't_statistic': float(tstat),
            'p_value': float(pval),
            'significant': pval < 0.05
        },
        'iron_distribution': {
            'vein': {level: int(iron_distribution.loc['vein', level]) if 'vein' in iron_distribution.index else 0 
                    for level in ['low', 'normal', 'high']},
            'artery': {level: int(iron_distribution.loc['artery', level]) if 'artery' in iron_distribution.index else 0 
                      for level in ['low', 'normal', 'high']}
        },
        'iron_test': {
            'chi2': float(chi2),
            'p_value': float(pval_iron),
            'significant': pval_iron < 0.05
        },
        'total_samples': len(lifespans)
    }
    
    return results

if __name__ == '__main__':
    results = analyze_familiar()
    print(json.dumps(results, indent=2))

