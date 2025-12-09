"""
US Census Data Analysis
Cleans and analyzes US census data including income, population, and demographics
"""

import pandas as pd
import numpy as np
import json
import os
import glob

def load_census_data():
    """Load census data from CSV files"""
    try:
        # Try to find states*.csv files
        state_files = glob.glob(os.path.join('csv', 'states*.csv'))
        if not state_files:
            state_files = glob.glob('states*.csv')
        
        if state_files:
            # Sort files to ensure consistent order
            state_files = sorted(state_files)
            df_list = [pd.read_csv(fname) for fname in state_files]
            df = pd.concat(df_list, ignore_index=True)
            # Drop the 'Unnamed: 0' column if it exists
            if 'Unnamed: 0' in df.columns:
                df = df.drop(columns=['Unnamed: 0'])
            return clean_census_data(df)
        else:
            return generate_sample_census_data()
    except Exception as e:
        print(f"Error loading census data: {e}")
        return generate_sample_census_data()

def clean_census_data(df):
    """Clean census data"""
    # Clean Income column - handle empty strings and NaN
    if 'Income' in df.columns:
        # Convert to string first to handle all cases
        df['Income'] = df['Income'].astype(str)
        # Replace empty strings and whitespace with NaN
        df['Income'] = df['Income'].replace(['', 'nan', 'NaN', 'None'], pd.NA)
        # Remove $ and commas
        df['Income'] = df['Income'].str.replace(r'[\$,]', '', regex=True)
        # Remove any remaining whitespace
        df['Income'] = df['Income'].str.strip()
        # Replace empty strings again after cleaning
        df['Income'] = df['Income'].replace('', pd.NA)
        # Convert to float, handling NaN and empty strings
        df['Income'] = pd.to_numeric(df['Income'], errors='coerce')
        # Fill NaN with mean if needed
        if df['Income'].isna().any():
            mean_income = df['Income'].mean()
            if pd.notna(mean_income):
                df['Income'] = df['Income'].fillna(mean_income)
            else:
                df['Income'] = df['Income'].fillna(50000)  # Default fallback
    
    # Split GenderPop if it exists
    if 'GenderPop' in df.columns:
        gender_split = df['GenderPop'].str.split('_', expand=True)
        df['Men'] = gender_split[0].replace(r'[MF]', '', regex=True).astype(float)
        df['Women'] = gender_split[1].replace(r'[MF]', '', regex=True).astype(float)
        
        # Fill missing Women using TotalPop - Men
        if 'TotalPop' in df.columns:
            df.loc[df['Women'].isna(), 'Women'] = df['TotalPop'] - df['Men']
    
    # Clean race percentage columns
    race_cols = ['Hispanic', 'White', 'Black', 'Native', 'Asian', 'Pacific']
    for col in race_cols:
        if col in df.columns:
            df[col] = df[col].replace(r'[%]', '', regex=True).astype(float)
            df[col] = df[col].fillna(df[col].mean())
    
    # Drop duplicates
    df = df.drop_duplicates()
    
    return df

def generate_sample_census_data():
    """Generate sample US census data for demonstration"""
    np.random.seed(42)
    
    states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 
              'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
              'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
              'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
              'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
              'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
              'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
              'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
              'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
              'West Virginia', 'Wisconsin', 'Wyoming']
    
    data = []
    for state in states:
        total_pop = np.random.randint(500000, 40000000)
        men = int(total_pop * np.random.uniform(0.48, 0.52))
        women = total_pop - men
        
        income = np.random.uniform(30000, 80000)
        
        # Race percentages (should sum to ~100)
        hispanic = np.random.uniform(5, 50)
        white = np.random.uniform(40, 90)
        black = np.random.uniform(5, 40)
        native = np.random.uniform(0.5, 5)
        asian = np.random.uniform(1, 15)
        pacific = np.random.uniform(0.1, 2)
        
        data.append({
            'State': state,
            'TotalPop': total_pop,
            'Men': men,
            'Women': women,
            'Income': income,
            'Hispanic': hispanic,
            'White': white,
            'Black': black,
            'Native': native,
            'Asian': asian,
            'Pacific': pacific
        })
    
    return pd.DataFrame(data)

def analyze_census():
    """Analyze census data and return results"""
    df = load_census_data()
    
    # Women vs Income scatter data
    women_income_data = df[['Women', 'Income']].to_dict('records')
    
    # Race percentage distributions
    race_cols = ['Hispanic', 'White', 'Black', 'Native', 'Asian', 'Pacific']
    race_distributions = {}
    for col in race_cols:
        if col in df.columns:
            race_distributions[col] = df[col].tolist()
    
    # Summary statistics
    summary = {
        'total_states': len(df),
        'avg_income': float(df['Income'].mean()) if 'Income' in df.columns else 0,
        'avg_population': float(df['TotalPop'].mean()) if 'TotalPop' in df.columns else 0,
        'avg_women': float(df['Women'].mean()) if 'Women' in df.columns else 0,
        'avg_men': float(df['Men'].mean()) if 'Men' in df.columns else 0
    }
    
    # Race averages
    race_averages = {}
    for col in race_cols:
        if col in df.columns:
            race_averages[col] = float(df[col].mean())
    
    results = {
        'women_income_data': women_income_data,
        'race_distributions': {k: [float(v2) for v2 in v] for k, v in race_distributions.items()},
        'summary': summary,
        'race_averages': race_averages,
        'states': df['State'].tolist() if 'State' in df.columns else []
    }
    
    return results

if __name__ == '__main__':
    results = analyze_census()
    print(json.dumps(results, indent=2))

