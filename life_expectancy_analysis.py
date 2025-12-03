"""
Life Expectancy and GDP Analysis
Analyzes the relationship between GDP and life expectancy across countries
"""

import pandas as pd
import numpy as np
import json
import os

def load_life_expectancy_data():
    """Load life expectancy and GDP data from CSV file"""
    try:
        csv_path = os.path.join('data', 'all_data.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
        else:
            df = generate_sample_life_expectancy_data()
        return df
    except Exception as e:
        print(f"Error loading life expectancy data: {e}")
        return generate_sample_life_expectancy_data()

def generate_sample_life_expectancy_data():
    """Generate sample life expectancy and GDP data for demonstration"""
    np.random.seed(42)
    
    countries = ['Chile', 'China', 'Germany', 'Mexico', 'United States of America', 'Zimbabwe']
    years = list(range(2000, 2016))
    
    data = []
    for country in countries:
        # Base life expectancy varies by country
        base_le = {
            'Chile': 75,
            'China': 72,
            'Germany': 78,
            'Mexico': 74,
            'United States of America': 77,
            'Zimbabwe': 45
        }[country]
        
        # Base GDP varies by country
        base_gdp = {
            'Chile': 15000,
            'China': 5000,
            'Germany': 35000,
            'Mexico': 10000,
            'United States of America': 45000,
            'Zimbabwe': 500
        }[country]
        
        for year in years:
            # Life expectancy increases slightly over time
            le = base_le + (year - 2000) * 0.3 + np.random.normal(0, 1)
            
            # GDP increases over time with some variation
            gdp = base_gdp * (1 + (year - 2000) * 0.05) + np.random.normal(0, base_gdp * 0.1)
            
            data.append({
                'Country': country,
                'Year': year,
                'Life expectancy at birth (years)': max(40, le),
                'GDP': max(100, gdp)
            })
    
    return pd.DataFrame(data)

def analyze_life_expectancy():
    """Analyze life expectancy and GDP data"""
    df = load_life_expectancy_data()
    
    # Summary by country
    summary_by_country = {}
    for country in df['Country'].unique():
        country_data = df[df['Country'] == country]
        summary_by_country[country] = {
            'Life expectancy at birth (years)': {
                'mean': float(country_data['Life expectancy at birth (years)'].mean()),
                'min': float(country_data['Life expectancy at birth (years)'].min()),
                'max': float(country_data['Life expectancy at birth (years)'].max())
            },
            'GDP': {
                'mean': float(country_data['GDP'].mean()),
                'min': float(country_data['GDP'].min()),
                'max': float(country_data['GDP'].max())
            }
        }
    
    # Overall correlation
    correlation = float(df['Life expectancy at birth (years)'].corr(df['GDP']))
    
    # Life expectancy distribution by country
    life_expectancy_by_country = {}
    for country in df['Country'].unique():
        life_expectancy_by_country[country] = df[df['Country'] == country]['Life expectancy at birth (years)'].tolist()
    
    # GDP vs Life Expectancy by country
    gdp_life_by_country = {}
    for country in df['Country'].unique():
        country_data = df[df['Country'] == country]
        gdp_life_by_country[country] = {
            'gdp': country_data['GDP'].tolist(),
            'life_expectancy': country_data['Life expectancy at birth (years)'].tolist()
        }
    
    # GDP over time by country
    gdp_over_time = {}
    for country in df['Country'].unique():
        country_data = df[df['Country'] == country].sort_values('Year')
        gdp_over_time[country] = {
            'years': country_data['Year'].tolist(),
            'gdp': country_data['GDP'].tolist()
        }
    
    # Life expectancy over time by country
    life_over_time = {}
    for country in df['Country'].unique():
        country_data = df[df['Country'] == country].sort_values('Year')
        life_over_time[country] = {
            'years': country_data['Year'].tolist(),
            'life_expectancy': country_data['Life expectancy at birth (years)'].tolist()
        }
    
    # Convert summary_by_country to JSON-serializable format
    summary_serialized = {}
    for country, stats in summary_by_country.items():
        summary_serialized[str(country)] = {
            'Life expectancy at birth (years)': {
                'mean': stats['Life expectancy at birth (years)']['mean'],
                'min': stats['Life expectancy at birth (years)']['min'],
                'max': stats['Life expectancy at birth (years)']['max']
            },
            'GDP': {
                'mean': stats['GDP']['mean'],
                'min': stats['GDP']['min'],
                'max': stats['GDP']['max']
            }
        }
    
    results = {
        'summary_by_country': summary_serialized,
        'correlation': correlation,
        'life_expectancy_by_country': {str(k): [float(v2) for v2 in v] for k, v in life_expectancy_by_country.items()},
        'gdp_life_by_country': {str(k): {'gdp': [float(v2) for v2 in v['gdp']], 'life_expectancy': [float(v2) for v2 in v['life_expectancy']]} for k, v in gdp_life_by_country.items()},
        'gdp_over_time': {str(k): {'years': [int(v2) for v2 in v['years']], 'gdp': [float(v2) for v2 in v['gdp']]} for k, v in gdp_over_time.items()},
        'life_over_time': {str(k): {'years': [int(v2) for v2 in v['years']], 'life_expectancy': [float(v2) for v2 in v['life_expectancy']]} for k, v in life_over_time.items()},
        'countries': [str(c) for c in df['Country'].unique()],
        'years': [int(y) for y in sorted(df['Year'].unique())]
    }
    
    return results

if __name__ == '__main__':
    results = analyze_life_expectancy()
    print(json.dumps(results, indent=2))

