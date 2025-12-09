"""
Biodiversity in National Parks Analysis
Analyzes species conservation status and observations in national parks
"""

import pandas as pd
import numpy as np
import json
import os
from scipy.stats import chi2_contingency

def load_biodiversity_data():
    """Load biodiversity data"""
    try:
        species_path = os.path.join('csv', 'species_info.csv')
        observations_path = os.path.join('csv', 'observations.csv')
        
        if os.path.exists(species_path) and os.path.exists(observations_path):
            species = pd.read_csv(species_path)
            observations = pd.read_csv(observations_path)
            return species, observations
        else:
            return generate_sample_biodiversity_data()
    except Exception as e:
        print(f"Error loading biodiversity data: {e}")
        return generate_sample_biodiversity_data()

def generate_sample_biodiversity_data():
    """Generate sample biodiversity data"""
    np.random.seed(42)
    
    categories = ['Mammal', 'Bird', 'Reptile', 'Amphibian', 'Fish', 'Vascular Plant', 'Nonvascular Plant']
    conservation_statuses = ['No Intervention', 'Species of Concern', 'Endangered', 'Threatened', 'In Recovery']
    parks = ['Great Smoky Mountains National Park', 'Yosemite National Park', 
             'Bryce National Park', 'Yellowstone National Park']
    
    # Generate species data
    n_species = 500
    species_data = []
    for i in range(n_species):
        species_data.append({
            'scientific_name': f'Species_{i}',
            'common_name': f'Common Name {i}',
            'category': np.random.choice(categories),
            'conservation_status': np.random.choice(conservation_statuses, p=[0.7, 0.15, 0.08, 0.05, 0.02])
        })
    
    species = pd.DataFrame(species_data)
    species['conservation_status'] = species['conservation_status'].fillna('No Intervention')
    
    # Generate observations data
    observations_data = []
    for park in parks:
        for sci_name in species['scientific_name'].sample(200):
            observations_data.append({
                'scientific_name': sci_name,
                'park_name': park,
                'observations': np.random.randint(0, 1000)
            })
    
    observations = pd.DataFrame(observations_data)
    
    return species, observations

def analyze_biodiversity():
    """Analyze biodiversity data and return results for visualization"""
    species, observations = load_biodiversity_data()
    
    # Conservation status distribution
    status_counts = (
        species.groupby('conservation_status')['scientific_name']
        .nunique()
        .reset_index()
        .rename(columns={'scientific_name': 'species_count'})
        .sort_values('species_count', ascending=False)
    )
    
    # Category protection analysis
    species['is_protected'] = species['conservation_status'] != 'No Intervention'
    category_protection = (
        species.groupby(['category', 'is_protected'])['scientific_name']
        .nunique()
        .reset_index()
        .rename(columns={'scientific_name': 'species_count'})
    )
    
    category_pivot = category_protection.pivot(
        index='category',
        columns='is_protected',
        values='species_count'
    ).fillna(0)
    
    category_pivot.columns = ['not_protected', 'protected']
    category_pivot['total'] = category_pivot['not_protected'] + category_pivot['protected']
    category_pivot['percent_protected'] = (category_pivot['protected'] / category_pivot['total'] * 100).round(2)
    
    # Chi-square test between categories
    chi_square_results = {}
    categories_list = category_pivot.index.tolist()
    for i in range(min(3, len(categories_list))):
        for j in range(i+1, min(4, len(categories_list))):
            cat1, cat2 = categories_list[i], categories_list[j]
            try:
                sub = category_pivot.loc[[cat1, cat2], ['protected', 'not_protected']]
                contingency = sub.values
                chi2, pval, dof, expected = chi2_contingency(contingency)
                chi_square_results[f'{cat1}_vs_{cat2}'] = {
                    'chi2': float(chi2),
                    'p_value': float(pval),
                    'significant': pval < 0.05
                }
            except:
                pass
    
    # Merge species and observations
    merged = observations.merge(
        species[['scientific_name', 'common_name', 'category', 'is_protected']],
        on='scientific_name',
        how='left'
    )
    
    # Top species by observations
    species_park_obs = (
        merged.groupby(['park_name', 'common_name', 'category', 'is_protected'])['observations']
        .sum()
        .reset_index()
    )
    
    top_species = (
        species_park_obs
        .sort_values('observations', ascending=False)
        .head(10)
    )
    
    # Top species per park
    top_per_park = (
        species_park_obs
        .sort_values(['park_name', 'observations'], ascending=[True, False])
        .groupby('park_name')
        .head(5)
    )
    
    results = {
        'status_distribution': {
            'statuses': status_counts['conservation_status'].tolist(),
            'counts': [int(c) for c in status_counts['species_count'].tolist()]
        },
        'category_protection': {
            'categories': category_pivot.index.tolist(),
            'percent_protected': [float(p) for p in category_pivot['percent_protected'].tolist()],
            'protected_counts': [int(c) for c in category_pivot['protected'].tolist()],
            'total_counts': [int(c) for c in category_pivot['total'].tolist()]
        },
        'chi_square_results': chi_square_results,
        'top_species': top_species[['common_name', 'category', 'observations']].to_dict('records'),
        'top_per_park': top_per_park.to_dict('records'),
        'total_species': len(species),
        'total_observations': int(observations['observations'].sum())
    }
    
    return results

if __name__ == '__main__':
    results = analyze_biodiversity()
    print(json.dumps(results, indent=2))

