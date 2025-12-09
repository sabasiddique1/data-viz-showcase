"""
Honey Production Linear Regression Analysis
Analyzes honey production trends and predicts future production
"""

import pandas as pd
import numpy as np
import json
import os
from sklearn.linear_model import LinearRegression

def load_honey_data():
    """Load honey production data"""
    try:
        # Try to download from URL
        df = pd.read_csv(
            "https://content.codecademy.com/programs/data-science-path/linear_regression/honeyproduction.csv"
        )
        return df
    except:
        # Generate sample data if download fails
        return generate_sample_honey_data()

def generate_sample_honey_data():
    """Generate sample honey production data"""
    np.random.seed(42)
    years = list(range(1998, 2013))
    data = []
    for year in years:
        for state in ['Alabama', 'California', 'Florida', 'Texas', 'New York']:
            data.append({
                'year': year,
                'state': state,
                'numcol': np.random.randint(5000, 50000),
                'yieldpercol': np.random.uniform(40, 80),
                'totalprod': np.random.uniform(200000, 2000000),
                'stocks': np.random.uniform(50000, 500000),
                'priceperlb': np.random.uniform(1.0, 3.0),
                'prodvalue': np.random.uniform(200000, 2000000)
            })
    return pd.DataFrame(data)

def analyze_honey_production():
    """Analyze honey production data and return results for visualization"""
    df = load_honey_data()
    
    # Group by year and get mean total production
    prod_per_year = df.groupby('year')['totalprod'].mean().reset_index()
    
    # Prepare data for regression
    X = prod_per_year['year'].values.reshape(-1, 1)
    y = prod_per_year['totalprod'].values
    
    # Create and fit linear regression model
    regr = LinearRegression()
    regr.fit(X, y)
    
    # Predict existing values
    y_predict = regr.predict(X)
    
    # Predict future years (2013-2050)
    X_future = np.array(range(2013, 2051)).reshape(-1, 1)
    future_predict = regr.predict(X_future)
    
    # Prepare data for charts
    historical_data = {
        'years': [int(year) for year in prod_per_year['year'].values],
        'actual': [float(val) for val in y],
        'predicted': [float(val) for val in y_predict]
    }
    
    future_data = {
        'years': [int(year) for year in X_future.flatten()],
        'predicted': [float(val) for val in future_predict]
    }
    
    results = {
        'slope': float(regr.coef_[0]),
        'intercept': float(regr.intercept_),
        'historical_data': historical_data,
        'future_data': future_data,
        'prediction_2050': float(future_predict[-1]),
        'current_avg': float(y.mean()),
        'stats': {
            'min_production': float(y.min()),
            'max_production': float(y.max()),
            'mean_production': float(y.mean()),
            'std_production': float(np.std(y))
        }
    }
    
    return results

if __name__ == '__main__':
    results = analyze_honey_production()
    print(json.dumps(results, indent=2))

