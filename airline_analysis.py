"""
Airline Analysis
Analyzes airline flight data including prices, delays, and inflight features
"""

import pandas as pd
import numpy as np
import json
import os

def load_airline_data():
    """Load airline data from CSV file"""
    try:
        csv_path = os.path.join('csv', 'flight.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            # Convert Yes/No strings to boolean for inflight features
            boolean_columns = ['inflight_meal', 'inflight_entertainment', 'inflight_wifi', 'redeye', 'weekend']
            for col in boolean_columns:
                if col in df.columns:
                    df[col] = df[col].map({'Yes': True, 'No': False, True: True, False: False}).fillna(False)
            return df
        else:
            df = generate_sample_airline_data()
        return df
    except Exception as e:
        print(f"Error loading airline data: {e}")
        return generate_sample_airline_data()

def generate_sample_airline_data():
    """Generate sample airline data for demonstration"""
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'miles': np.random.randint(200, 5000, n_samples),
        'passengers': np.random.randint(50, 300, n_samples),
        'delay': np.random.exponential(15, n_samples).astype(int),
        'inflight_meal': np.random.choice([True, False], n_samples, p=[0.6, 0.4]),
        'inflight_entertainment': np.random.choice([True, False], n_samples, p=[0.7, 0.3]),
        'inflight_wifi': np.random.choice([True, False], n_samples, p=[0.5, 0.5]),
        'day_of_week': np.random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], n_samples),
        'weekend': np.random.choice([True, False], n_samples, p=[0.3, 0.7]),
        'hours': np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], n_samples),
        'redeye': np.random.choice([True, False], n_samples, p=[0.2, 0.8])
    }
    
    # Generate prices based on features
    base_coach = 200
    data['coach_price'] = (
        base_coach + 
        data['miles'] * 0.1 + 
        data['hours'] * 20 +
        np.where(data['inflight_meal'], 30, 0) +
        np.where(data['inflight_entertainment'], 25, 0) +
        np.where(data['inflight_wifi'], 20, 0) +
        np.where(data['weekend'], 50, 0) +
        np.where(data['redeye'], -30, 0) +
        np.random.normal(0, 30, n_samples)
    )
    data['coach_price'] = np.maximum(data['coach_price'], 100)
    
    data['firstclass_price'] = data['coach_price'] * 2.5 + np.random.normal(0, 50, n_samples)
    data['firstclass_price'] = np.maximum(data['firstclass_price'], 300)
    
    return pd.DataFrame(data)

def analyze_airline():
    """Analyze airline data and return results for visualization"""
    df = load_airline_data()
    
    # Coach price statistics
    coach_stats = {
        'mean': float(df['coach_price'].mean()),
        'median': float(df['coach_price'].median()),
        'min': float(df['coach_price'].min()),
        'max': float(df['coach_price'].max()),
        'std': float(df['coach_price'].std())
    }
    
    # 8-hour flight prices
    eight_hour = df[df['hours'] == 8]
    eight_hour_stats = {
        'mean': float(eight_hour['coach_price'].mean()) if len(eight_hour) > 0 else 0,
        'median': float(eight_hour['coach_price'].median()) if len(eight_hour) > 0 else 0,
        'min': float(eight_hour['coach_price'].min()) if len(eight_hour) > 0 else 0,
        'max': float(eight_hour['coach_price'].max()) if len(eight_hour) > 0 else 0,
        'count': len(eight_hour)
    }
    
    # Delay distribution
    delay_max = df['delay'].max()
    if delay_max > 0:
        delay_bins = np.linspace(0, delay_max, 40)
        delay_hist, _ = np.histogram(df['delay'], bins=delay_bins)
    else:
        delay_bins = np.array([0])
        delay_hist = np.array([0])
    
    # Coach vs First-class relationship
    coach_first_data = df[['coach_price', 'firstclass_price']].to_dict('records')
    
    # Inflight features impact
    meal_impact = {
        'with_meal': float(df[df['inflight_meal']]['coach_price'].mean()),
        'without_meal': float(df[~df['inflight_meal']]['coach_price'].mean())
    }
    
    entertainment_impact = {
        'with_entertainment': float(df[df['inflight_entertainment']]['coach_price'].mean()),
        'without_entertainment': float(df[~df['inflight_entertainment']]['coach_price'].mean())
    }
    
    wifi_impact = {
        'with_wifi': float(df[df['inflight_wifi']]['coach_price'].mean()),
        'without_wifi': float(df[~df['inflight_wifi']]['coach_price'].mean())
    }
    
    # Passengers vs hours
    passengers_hours = df.groupby('hours')['passengers'].mean().to_dict()
    
    # Weekend vs weekday
    weekend_data = df.groupby('weekend').agg({
        'coach_price': 'mean',
        'firstclass_price': 'mean'
    }).to_dict()
    
    # Redeye by day of week
    redeye_by_day = df.groupby(['day_of_week', 'redeye'])['coach_price'].mean().unstack(fill_value=0).to_dict()
    
    results = {
        'coach_stats': coach_stats,
        'eight_hour_stats': eight_hour_stats,
        'delay_distribution': {
            'bins': [float(b) for b in delay_bins[:-1]] if len(delay_bins) > 1 else [0.0],
            'counts': [int(c) for c in delay_hist],
            'avg_delay': float(df['delay'].mean())
        },
        'coach_first_data': coach_first_data[:100],  # Sample for performance
        'meal_impact': meal_impact,
        'entertainment_impact': entertainment_impact,
        'wifi_impact': wifi_impact,
        'passengers_hours': {str(k): float(v) for k, v in passengers_hours.items()},
        'weekend_data': {str(k): {str(k2): float(v2) for k2, v2 in v.items()} for k, v in weekend_data.items()},
        'redeye_by_day': {str(k): {str(k2): float(v2) for k2, v2 in v.items()} if isinstance(v, dict) else float(v) for k, v in redeye_by_day.items()},
        'total_flights': len(df)
    }
    
    return results

if __name__ == '__main__':
    results = analyze_airline()
    print(json.dumps(results, indent=2))

