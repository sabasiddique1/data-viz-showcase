"""
Feature Transformation Analysis
Transforms categorical review data into numeric features for machine learning
"""

import pandas as pd
import numpy as np
import json
import os
from sklearn.preprocessing import StandardScaler

def load_reviews_data():
    """Load reviews data"""
    try:
        csv_path = os.path.join('csv', 'reviews.csv')
        if os.path.exists(csv_path):
            return pd.read_csv(csv_path)
        else:
            return generate_sample_reviews_data()
    except Exception as e:
        print(f"Error loading reviews data: {e}")
        return generate_sample_reviews_data()

def generate_sample_reviews_data():
    """Generate sample reviews data"""
    np.random.seed(42)
    n_samples = 500
    
    departments = ['Tops', 'Dresses', 'Bottoms', 'Intimate', 'Jackets', 'Trend']
    ratings = ['Loved it', 'Liked it', 'Was okay', 'Not great', 'Hated it']
    
    data = {
        'clothing_id': range(1, n_samples + 1),
        'recommended': np.random.choice([True, False], n_samples, p=[0.7, 0.3]),
        'rating': np.random.choice(ratings, n_samples, p=[0.3, 0.3, 0.2, 0.15, 0.05]),
        'department_name': np.random.choice(departments, n_samples),
        'review_date': pd.date_range('2020-01-01', periods=n_samples, freq='D')
    }
    
    return pd.DataFrame(data)

def analyze_feature_transformation():
    """Transform features and return results for visualization"""
    reviews = load_reviews_data()
    
    # Original data stats
    original_stats = {
        'total_reviews': len(reviews),
        'recommended_counts': reviews['recommended'].value_counts().to_dict(),
        'rating_counts': reviews['rating'].value_counts().to_dict(),
        'department_counts': reviews['department_name'].value_counts().to_dict()
    }
    
    # Transform recommended to binary
    binary_dict = {True: 1, False: 0}
    reviews['recommended_binary'] = reviews['recommended'].map(binary_dict)
    
    # Transform rating to numeric
    rating_dict = {
        'Loved it': 5,
        'Liked it': 4,
        'Was okay': 3,
        'Not great': 2,
        'Hated it': 1
    }
    reviews['rating_numeric'] = reviews['rating'].map(rating_dict)
    
    # One-hot encode department_name
    one_hot = pd.get_dummies(reviews['department_name'])
    reviews_encoded = reviews.join(one_hot)
    
    # Convert review_date to datetime
    reviews_encoded['review_date'] = pd.to_datetime(reviews_encoded['review_date'])
    
    # Keep only numerical features
    numeric_reviews = reviews_encoded[
        ['recommended_binary', 'rating_numeric'] + list(one_hot.columns)
    ]
    numeric_reviews.index = reviews_encoded['clothing_id']
    
    # Scale the data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numeric_reviews)
    
    # Prepare visualization data
    transformation_summary = {
        'binary_transformation': {
            'original': {str(k): int(v) for k, v in original_stats['recommended_counts'].items()},
            'transformed': {str(k): int(v) for k, v in reviews['recommended_binary'].value_counts().to_dict().items()}
        },
        'rating_transformation': {
            'original': {str(k): int(v) for k, v in original_stats['rating_counts'].items()},
            'transformed': {str(k): int(v) for k, v in reviews['rating_numeric'].value_counts().to_dict().items()}
        },
        'one_hot_encoding': {
            'departments': list(one_hot.columns),
            'sample_counts': {col: int(reviews_encoded[col].sum()) for col in one_hot.columns}
        },
        'scaling_stats': {
            'mean': float(np.mean(scaled_data)),
            'std': float(np.std(scaled_data)),
            'min': float(np.min(scaled_data)),
            'max': float(np.max(scaled_data))
        }
    }
    
    results = {
        'original_stats': original_stats,
        'transformation_summary': transformation_summary,
        'feature_count': len(numeric_reviews.columns),
        'sample_size': len(reviews)
    }
    
    return results

if __name__ == '__main__':
    results = analyze_feature_transformation()
    print(json.dumps(results, indent=2))

