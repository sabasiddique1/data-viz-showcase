"""
Exploring Mushrooms Analysis
Analyzes mushroom dataset and creates countplots for categorical features
"""

import pandas as pd
import json
import os

def load_mushroom_data():
    """Load mushroom data from CSV file"""
    try:
        # Try to load from data directory first
        csv_path = os.path.join('data', 'mushroom_data.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            # Convert column names to lowercase with hyphens for consistency
            # Original: "Cap Shape" -> "cap-shape", "Class" -> "class"
            df.columns = df.columns.str.lower().str.replace(' ', '-')
            # Handle special case: "Class" column might be "class" already
            return df
        else:
            # Generate sample data if file doesn't exist
            df = generate_sample_mushroom_data()
        return df
    except Exception as e:
        print(f"Error loading mushroom data: {e}")
        return generate_sample_mushroom_data()

def generate_sample_mushroom_data():
    """Generate sample mushroom data for demonstration"""
    import numpy as np
    
    n_samples = 8124
    np.random.seed(42)
    
    data = {
        'class': np.random.choice(['e', 'p'], n_samples, p=[0.52, 0.48]),
        'cap-shape': np.random.choice(['b', 'c', 'x', 'f', 'k', 's'], n_samples),
        'cap-surface': np.random.choice(['f', 'g', 'y', 's'], n_samples),
        'cap-color': np.random.choice(['n', 'b', 'c', 'g', 'r', 'p', 'u', 'e', 'w', 'y'], n_samples),
        'bruises': np.random.choice(['t', 'f'], n_samples, p=[0.48, 0.52]),
        'odor': np.random.choice(['a', 'l', 'c', 'y', 'f', 'm', 'n', 'p', 's'], n_samples),
        'gill-attachment': np.random.choice(['a', 'd', 'f', 'n'], n_samples),
        'gill-spacing': np.random.choice(['c', 'w', 'd'], n_samples),
        'gill-size': np.random.choice(['b', 'n'], n_samples, p=[0.56, 0.44]),
        'gill-color': np.random.choice(['k', 'n', 'b', 'h', 'g', 'r', 'o', 'p', 'u', 'e', 'w', 'y'], n_samples),
        'stalk-shape': np.random.choice(['e', 't'], n_samples, p=[0.52, 0.48]),
        'stalk-root': np.random.choice(['b', 'c', 'u', 'e', 'z', 'r', '?'], n_samples),
        'stalk-surface-above-ring': np.random.choice(['f', 'y', 'k', 's'], n_samples),
        'stalk-surface-below-ring': np.random.choice(['f', 'y', 'k', 's'], n_samples),
        'stalk-color-above-ring': np.random.choice(['n', 'b', 'c', 'g', 'o', 'p', 'e', 'w', 'y'], n_samples),
        'stalk-color-below-ring': np.random.choice(['n', 'b', 'c', 'g', 'o', 'p', 'e', 'w', 'y'], n_samples),
        'veil-type': np.random.choice(['p'], n_samples),
        'veil-color': np.random.choice(['n', 'o', 'w', 'y'], n_samples),
        'ring-number': np.random.choice(['n', 'o', 't'], n_samples),
        'ring-type': np.random.choice(['c', 'e', 'f', 'l', 'n', 'p', 's', 'z'], n_samples),
        'spore-print-color': np.random.choice(['k', 'n', 'b', 'h', 'r', 'o', 'u', 'w', 'y'], n_samples),
        'population': np.random.choice(['a', 'c', 'n', 's', 'v', 'y'], n_samples),
        'habitat': np.random.choice(['g', 'l', 'm', 'p', 'u', 'w', 'd'], n_samples)
    }
    
    return pd.DataFrame(data)

def should_plot(column_values, threshold=20):
    """Return True if the column has <= threshold unique values"""
    return column_values.nunique() <= threshold

def analyze_mushrooms():
    """Analyze mushroom data and return results for visualization"""
    df = load_mushroom_data()
    
    results = {
        'total_samples': len(df),
        'columns': [],
        'column_stats': {}
    }
    
    # Analyze each column
    for column in df.columns:
        unique_count = df[column].nunique()
        if should_plot(df[column], threshold=20):
            value_counts_series = df[column].value_counts()
            value_counts = value_counts_series.to_dict()
            results['columns'].append(column)
            results['column_stats'][column] = {
                'unique_count': int(unique_count),
                'value_counts': {str(k): int(v) for k, v in value_counts.items()},
                'labels': [str(k) for k in value_counts_series.index],
                'values': [int(v) for v in value_counts_series.values]
            }
    
    return results

if __name__ == '__main__':
    results = analyze_mushrooms()
    print(json.dumps(results, indent=2))

