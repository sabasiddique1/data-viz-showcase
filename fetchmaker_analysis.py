"""
Fetchmaker Dog Data Analysis
Analyzes dog breed characteristics and traits
"""

import pandas as pd
import numpy as np
import json
import os
from scipy.stats import chi2_contingency

def load_dog_data():
    """Load dog data"""
    try:
        csv_path = os.path.join('csv', 'dog_data.csv')
        if os.path.exists(csv_path):
            return pd.read_csv(csv_path)
        else:
            return generate_sample_dog_data()
    except Exception as e:
        print(f"Error loading dog data: {e}")
        return generate_sample_dog_data()

def generate_sample_dog_data():
    """Generate sample dog data"""
    np.random.seed(42)
    
    breeds = ['whippet', 'terrier', 'pitbull', 'poodle', 'shihtzu', 'chihuahua', 'labrador']
    colors = ['black', 'brown', 'gold', 'white', 'gray']
    
    n_samples = 500
    data = {
        'breed': np.random.choice(breeds, n_samples),
        'weight': np.random.uniform(5, 80, n_samples),
        'tail_length': np.random.uniform(0.5, 10, n_samples),
        'age': np.random.randint(1, 15, n_samples),
        'color': np.random.choice(colors, n_samples),
        'likes_children': np.random.choice([0, 1], n_samples, p=[0.3, 0.7]),
        'is_hypoallergenic': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
        'is_rescue': np.random.choice([0, 1], n_samples, p=[0.6, 0.4])
    }
    
    return pd.DataFrame(data)

def analyze_fetchmaker():
    """Analyze dog data and return results for visualization"""
    dogs = load_dog_data()
    
    # Subset to whippets, terriers, and pitbulls
    dogs_wtp = dogs[dogs['breed'].isin(['whippet', 'terrier', 'pitbull'])]
    
    # Subset to poodles and shihtzus
    dogs_ps = dogs[dogs['breed'].isin(['poodle', 'shihtzu'])]
    
    # Breed statistics
    breed_stats = dogs.groupby('breed').agg({
        'weight': ['mean', 'std'],
        'tail_length': ['mean', 'std'],
        'age': 'mean'
    }).round(2)
    
    # Weight comparison for whippets, terriers, pitbulls
    wtp_weight_stats = dogs_wtp.groupby('breed')['weight'].agg(['mean', 'std', 'count']).to_dict()
    
    # Hypoallergenic by breed
    hypo_by_breed = dogs.groupby(['breed', 'is_hypoallergenic']).size().unstack(fill_value=0)
    
    # Likes children by breed
    children_by_breed = dogs.groupby(['breed', 'likes_children']).size().unstack(fill_value=0)
    
    # Color distribution
    color_distribution = dogs['color'].value_counts().to_dict()
    
    # Age distribution by breed
    age_by_breed = dogs.groupby('breed')['age'].mean().to_dict()
    
    results = {
        'breed_stats': {
            'breeds': breed_stats.index.tolist(),
            'avg_weight': {breed: float(breed_stats.loc[breed, ('weight', 'mean')]) for breed in breed_stats.index},
            'avg_tail_length': {breed: float(breed_stats.loc[breed, ('tail_length', 'mean')]) for breed in breed_stats.index},
            'avg_age': {breed: float(breed_stats.loc[breed, ('age', 'mean')]) for breed in breed_stats.index}
        },
        'wtp_weight_comparison': {
            breed: {
                'mean': float(wtp_weight_stats['mean'].get(breed, 0)),
                'std': float(wtp_weight_stats['std'].get(breed, 0)),
                'count': int(wtp_weight_stats['count'].get(breed, 0))
            } for breed in ['whippet', 'terrier', 'pitbull']
        },
        'hypoallergenic_distribution': {
            breed: {
                'not_hypoallergenic': int(hypo_by_breed.loc[breed, 0]) if breed in hypo_by_breed.index else 0,
                'hypoallergenic': int(hypo_by_breed.loc[breed, 1]) if breed in hypo_by_breed.index else 0
            } for breed in hypo_by_breed.index
        },
        'children_preference': {
            breed: {
                'does_not_like': int(children_by_breed.loc[breed, 0]) if breed in children_by_breed.index else 0,
                'likes': int(children_by_breed.loc[breed, 1]) if breed in children_by_breed.index else 0
            } for breed in children_by_breed.index
        },
        'color_distribution': {str(k): int(v) for k, v in color_distribution.items()},
        'age_by_breed': {str(k): float(v) for k, v in age_by_breed.items()},
        'total_dogs': len(dogs)
    }
    
    return results

if __name__ == '__main__':
    results = analyze_fetchmaker()
    print(json.dumps(results, indent=2))

