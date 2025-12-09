"""
US Medical Insurance Cost Analysis (Class-Based Version)
========================================================

This version uses object-oriented programming to organize the analysis.
Great for portfolio projects and demonstrates OOP skills.
"""

import csv
import os


class InsuranceDataset:
    """A class to store and analyze medical insurance data."""
    
    def __init__(self, csv_file=None):
        """Initialize the dataset and load data from CSV."""
        if csv_file is None:
            csv_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'csv', 'insurance.csv')
        self.ages = []
        self.sexes = []
        self.bmis = []
        self.num_children = []
        self.smoker_statuses = []
        self.regions = []
        self.insurance_charges = []
        
        self.load_data(csv_file)
    
    def load_data(self, csv_file):
        """Load insurance data from CSV file into instance variables."""
        with open(csv_file) as insurance_file:
            reader = csv.DictReader(insurance_file)
            for row in reader:
                self.ages.append(int(row["age"]))
                self.sexes.append(row["sex"])
                self.bmis.append(float(row["bmi"]))
                self.num_children.append(int(row["children"]))
                self.smoker_statuses.append(row["smoker"])
                self.regions.append(row["region"])
                self.insurance_charges.append(float(row["charges"]))
        
        print(f"✓ Loaded {len(self.ages)} records from {csv_file}\n")
    
    @staticmethod
    def mean(values):
        """Return the average of a list of numbers."""
        return sum(values) / len(values)
    
    def basic_overview(self):
        """Print basic statistics about the dataset."""
        print("=" * 50)
        print("BASIC OVERVIEW")
        print("=" * 50)
        print(f"Number of records: {len(self.ages)}")
        print(f"Average age: {round(self.mean(self.ages), 1)} years")
        print(f"Average BMI: {round(self.mean(self.bmis), 1)}")
        print(f"Average number of children: {round(self.mean(self.num_children), 1)}")
        print(f"Average insurance charges: ${round(self.mean(self.insurance_charges), 2)}")
        print()
    
    def average_charges_by_smoker(self):
        """Calculate and display average charges for smokers vs non-smokers."""
        smoker_charges = [
            charge for status, charge in zip(self.smoker_statuses, self.insurance_charges)
            if status == "yes"
        ]
        non_smoker_charges = [
            charge for status, charge in zip(self.smoker_statuses, self.insurance_charges)
            if status == "no"
        ]
        
        print("=" * 50)
        print("AVERAGE CHARGES BY SMOKER STATUS")
        print("=" * 50)
        print(f"Smokers ({len(smoker_charges)} records):")
        print(f"  Average charges: ${round(self.mean(smoker_charges), 2)}")
        print(f"\nNon-smokers ({len(non_smoker_charges)} records):")
        print(f"  Average charges: ${round(self.mean(non_smoker_charges), 2)}")
        
        difference = self.mean(smoker_charges) - self.mean(non_smoker_charges)
        percentage = (difference / self.mean(non_smoker_charges)) * 100
        print(f"\nDifference: ${round(difference, 2)}")
        print(f"Smokers pay {round(percentage, 1)}% more on average")
        print()
    
    def average_charges_by_region(self):
        """Calculate and display average charges by region."""
        region_to_charges = {}
        
        for region, charge in zip(self.regions, self.insurance_charges):
            region_to_charges.setdefault(region, []).append(charge)
        
        print("=" * 50)
        print("AVERAGE CHARGES BY REGION")
        print("=" * 50)
        for region, charges in sorted(region_to_charges.items()):
            print(f"{region.capitalize():15s}: ${round(self.mean(charges), 2):>12,.2f} ({len(charges)} records)")
        print()
    
    def average_charges_by_sex(self):
        """Calculate and display average charges by sex."""
        male_charges = [
            charge for sex, charge in zip(self.sexes, self.insurance_charges)
            if sex == "male"
        ]
        female_charges = [
            charge for sex, charge in zip(self.sexes, self.insurance_charges)
            if sex == "female"
        ]
        
        print("=" * 50)
        print("AVERAGE CHARGES BY SEX")
        print("=" * 50)
        print(f"Male ({len(male_charges)} records):")
        print(f"  Average charges: ${round(self.mean(male_charges), 2)}")
        print(f"\nFemale ({len(female_charges)} records):")
        print(f"  Average charges: ${round(self.mean(female_charges), 2)}")
        
        difference = self.mean(male_charges) - self.mean(female_charges)
        percentage = (difference / self.mean(female_charges)) * 100
        print(f"\nDifference: ${round(difference, 2)}")
        print(f"Males pay {round(percentage, 1)}% more on average")
        print()
    
    def average_charges_by_bmi_category(self):
        """Calculate and display average charges by BMI category."""
        categories = {
            "Underweight": [],
            "Normal": [],
            "Overweight": [],
            "Obese": []
        }
        
        for bmi, charge in zip(self.bmis, self.insurance_charges):
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
            if charges:
                print(f"{cat:12s}: ${round(self.mean(charges), 2):>12,.2f} ({len(charges)} records)")
        print()
    
    def average_charges_by_age_group(self):
        """Calculate and display average charges by age group."""
        age_groups = {
            "18-30": [],
            "31-40": [],
            "41-50": [],
            "51-60": [],
            "60+": []
        }
        
        for age, charge in zip(self.ages, self.insurance_charges):
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
                print(f"{group:8s}: ${round(self.mean(charges), 2):>12,.2f} ({len(charges)} records)")
        print()
    
    def get_summary(self):
        """Return a dictionary with key summary statistics."""
        smoker_charges = [
            c for s, c in zip(self.smoker_statuses, self.insurance_charges) if s == "yes"
        ]
        non_smoker_charges = [
            c for s, c in zip(self.smoker_statuses, self.insurance_charges) if s == "no"
        ]
        
        region_charges = {}
        for r, c in zip(self.regions, self.insurance_charges):
            region_charges.setdefault(r, []).append(c)
        
        return {
            "total_records": len(self.ages),
            "avg_age": round(self.mean(self.ages), 1),
            "avg_bmi": round(self.mean(self.bmis), 1),
            "avg_charges": round(self.mean(self.insurance_charges), 2),
            "smoker_avg": round(self.mean(smoker_charges), 2) if smoker_charges else 0,
            "non_smoker_avg": round(self.mean(non_smoker_charges), 2) if non_smoker_charges else 0,
            "regions": {
                r: round(self.mean(charges), 2) 
                for r, charges in region_charges.items()
            }
        }
    
    def run_full_analysis(self):
        """Run all analysis methods in sequence."""
        print("\n" + "=" * 50)
        print("US MEDICAL INSURANCE COST ANALYSIS (Class-Based)")
        print("=" * 50 + "\n")
        
        self.basic_overview()
        self.average_charges_by_smoker()
        self.average_charges_by_region()
        self.average_charges_by_sex()
        self.average_charges_by_bmi_category()
        self.average_charges_by_age_group()
        
        print("=" * 50)
        print("Analysis complete!")
        print("=" * 50 + "\n")


# Main execution
if __name__ == "__main__":
    # Create dataset instance
    dataset = InsuranceDataset()  # Uses default path to csv/insurance.csv
    
    # Run full analysis
    dataset.run_full_analysis()
    
    # Example: Access summary data programmatically
    summary = dataset.get_summary()
    print("\nSummary Dictionary:")
    print(summary)


