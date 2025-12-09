"""
US Medical Insurance Cost Analysis
===================================

Project Goals:
1. Explore how medical charges differ by:
   - smoker vs non-smoker
   - region
   - sex
   - BMI category

2. Check relationships between:
   - age and charges
   - BMI and charges
   - number of children and charges

3. Make simple, human-readable conclusions (not full ML).
"""

# Import csv library
import csv

# Create empty lists for the various attributes in insurance.csv
ages = []
sexes = []
bmis = []
num_children = []
smoker_statuses = []
regions = []
insurance_charges = []


# Read data from insurance.csv
def load_data():
    """Load insurance data from CSV file into lists."""
    import os
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'csv', 'insurance.csv')
    with open(csv_path) as insurance_file:
        reader = csv.DictReader(insurance_file)
        for row in reader:
            ages.append(int(row["age"]))
            sexes.append(row["sex"])
            bmis.append(float(row["bmi"]))
            num_children.append(int(row["children"]))
            smoker_statuses.append(row["smoker"])
            regions.append(row["region"])
            insurance_charges.append(float(row["charges"]))
    
    print("✓ Data loaded successfully!")
    print(f"  Total records: {len(ages)}")
    print(f"  Sample ages: {ages[:5]}")
    print(f"  Sample charges: {insurance_charges[:5]}\n")


# Helper function: Calculate mean
def mean(values):
    """Return the average of a list of numbers."""
    return sum(values) / len(values)


# Basic overview statistics
def basic_overview():
    """Print basic statistics about the dataset."""
    print("=" * 50)
    print("BASIC OVERVIEW")
    print("=" * 50)
    print(f"Number of records: {len(ages)}")
    print(f"Average age: {round(mean(ages), 1)} years")
    print(f"Average BMI: {round(mean(bmis), 1)}")
    print(f"Average number of children: {round(mean(num_children), 1)}")
    print(f"Average insurance charges: ${round(mean(insurance_charges), 2)}")
    print()


# Analysis: Average charges by smoker status
def average_charges_by_smoker():
    """Calculate and display average charges for smokers vs non-smokers."""
    smoker_charges = []
    non_smoker_charges = []
    
    for status, charge in zip(smoker_statuses, insurance_charges):
        if status == "yes":
            smoker_charges.append(charge)
        else:
            non_smoker_charges.append(charge)
    
    print("=" * 50)
    print("AVERAGE CHARGES BY SMOKER STATUS")
    print("=" * 50)
    print(f"Smokers ({len(smoker_charges)} records):")
    print(f"  Average charges: ${round(mean(smoker_charges), 2)}")
    print(f"\nNon-smokers ({len(non_smoker_charges)} records):")
    print(f"  Average charges: ${round(mean(non_smoker_charges), 2)}")
    
    difference = mean(smoker_charges) - mean(non_smoker_charges)
    percentage = (difference / mean(non_smoker_charges)) * 100
    print(f"\nDifference: ${round(difference, 2)}")
    print(f"Smokers pay {round(percentage, 1)}% more on average")
    print()


# Analysis: Average charges by region
def average_charges_by_region():
    """Calculate and display average charges by region."""
    region_to_charges = {}
    
    for region, charge in zip(regions, insurance_charges):
        region_to_charges.setdefault(region, []).append(charge)
    
    print("=" * 50)
    print("AVERAGE CHARGES BY REGION")
    print("=" * 50)
    for region, charges in sorted(region_to_charges.items()):
        print(f"{region.capitalize():15s}: ${round(mean(charges), 2):>12,.2f} ({len(charges)} records)")
    print()


# Analysis: Average charges by sex
def average_charges_by_sex():
    """Calculate and display average charges by sex."""
    male_charges = []
    female_charges = []
    
    for sex, charge in zip(sexes, insurance_charges):
        if sex == "male":
            male_charges.append(charge)
        else:
            female_charges.append(charge)
    
    print("=" * 50)
    print("AVERAGE CHARGES BY SEX")
    print("=" * 50)
    print(f"Male ({len(male_charges)} records):")
    print(f"  Average charges: ${round(mean(male_charges), 2)}")
    print(f"\nFemale ({len(female_charges)} records):")
    print(f"  Average charges: ${round(mean(female_charges), 2)}")
    
    difference = mean(male_charges) - mean(female_charges)
    percentage = (difference / mean(female_charges)) * 100
    print(f"\nDifference: ${round(difference, 2)}")
    print(f"Males pay {round(percentage, 1)}% more on average")
    print()


# Analysis: Average charges by BMI category
def average_charges_by_bmi_category():
    """
    Calculate and display average charges by BMI category.
    
    Categories:
    - Underweight: BMI < 18.5
    - Normal: 18.5 ≤ BMI < 25
    - Overweight: 25 ≤ BMI < 30
    - Obese: BMI ≥ 30
    """
    categories = {
        "Underweight": [],
        "Normal": [],
        "Overweight": [],
        "Obese": []
    }
    
    for bmi, charge in zip(bmis, insurance_charges):
        if bmi < 18.5:
            categories["Underweight"].append(charge)
        elif bmi < 25:
            categories["Normal"].append(charge)
        elif bmi < 30:
            categories["Overweight"].append(charge)
        else:
            categories["Obese"].append(charge)
    
    print("=" * 50)
    print("AVERAGE CHARGES BY BMI CATEGORY")
    print("=" * 50)
    for cat, charges in categories.items():
        if charges:  # Only print if category has data
            print(f"{cat:12s}: ${round(mean(charges), 2):>12,.2f} ({len(charges)} records)")
    print()


# Analysis: Age groups and charges
def average_charges_by_age_group():
    """Calculate and display average charges by age group."""
    age_groups = {
        "18-30": [],
        "31-40": [],
        "41-50": [],
        "51-60": [],
        "60+": []
    }
    
    for age, charge in zip(ages, insurance_charges):
        if age <= 30:
            age_groups["18-30"].append(charge)
        elif age <= 40:
            age_groups["31-40"].append(charge)
        elif age <= 50:
            age_groups["41-50"].append(charge)
        elif age <= 60:
            age_groups["51-60"].append(charge)
        else:
            age_groups["60+"].append(charge)
    
    print("=" * 50)
    print("AVERAGE CHARGES BY AGE GROUP")
    print("=" * 50)
    for group, charges in age_groups.items():
        if charges:
            print(f"{group:8s}: ${round(mean(charges), 2):>12,.2f} ({len(charges)} records)")
    print()


# Analysis: Charges by number of children
def average_charges_by_children():
    """Calculate and display average charges by number of children."""
    children_to_charges = {}
    
    for num_kids, charge in zip(num_children, insurance_charges):
        children_to_charges.setdefault(num_kids, []).append(charge)
    
    print("=" * 50)
    print("AVERAGE CHARGES BY NUMBER OF CHILDREN")
    print("=" * 50)
    for num_kids in sorted(children_to_charges.keys()):
        charges = children_to_charges[num_kids]
        print(f"{num_kids} children: ${round(mean(charges), 2):>12,.2f} ({len(charges)} records)")
    print()


# Summary findings
def print_summary():
    """Print a summary of key findings."""
    print("=" * 50)
    print("KEY FINDINGS SUMMARY")
    print("=" * 50)
    
    # Smoker analysis
    smoker_charges = [c for s, c in zip(smoker_statuses, insurance_charges) if s == "yes"]
    non_smoker_charges = [c for s, c in zip(smoker_statuses, insurance_charges) if s == "no"]
    smoker_diff = mean(smoker_charges) - mean(non_smoker_charges)
    
    # Region analysis
    region_charges = {}
    for r, c in zip(regions, insurance_charges):
        region_charges.setdefault(r, []).append(c)
    highest_region = max(region_charges.items(), key=lambda x: mean(x[1]))
    lowest_region = min(region_charges.items(), key=lambda x: mean(x[1]))
    
    # BMI analysis
    obese_charges = [c for b, c in zip(bmis, insurance_charges) if b >= 30]
    normal_charges = [c for b, c in zip(bmis, insurance_charges) if 18.5 <= b < 25]
    
    print(f"1. Smoking has the biggest impact on costs:")
    print(f"   Smokers pay ${round(smoker_diff, 2)} more on average")
    print(f"   ({round((smoker_diff/mean(non_smoker_charges))*100, 1)}% increase)")
    
    print(f"\n2. Regional differences:")
    print(f"   Highest: {highest_region[0].capitalize()} (${round(mean(highest_region[1]), 2)})")
    print(f"   Lowest: {lowest_region[0].capitalize()} (${round(mean(lowest_region[1]), 2)})")
    
    if obese_charges and normal_charges:
        bmi_diff = mean(obese_charges) - mean(normal_charges)
        print(f"\n3. BMI impact:")
        print(f"   Obese individuals pay ${round(bmi_diff, 2)} more than normal BMI")
        print(f"   ({round((bmi_diff/mean(normal_charges))*100, 1)}% increase)")
    
    print()


# Main execution
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("US MEDICAL INSURANCE COST ANALYSIS")
    print("=" * 50 + "\n")
    
    # Load data
    load_data()
    
    # Run all analyses
    basic_overview()
    average_charges_by_smoker()
    average_charges_by_region()
    average_charges_by_sex()
    average_charges_by_bmi_category()
    average_charges_by_age_group()
    average_charges_by_children()
    print_summary()
    
    print("=" * 50)
    print("Analysis complete!")
    print("=" * 50 + "\n")


