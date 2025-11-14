# US Medical Insurance Cost Analysis

A comprehensive data analysis project exploring factors that influence medical insurance costs in the United States.

## 📋 Project Overview

This project analyzes a dataset of 1,338 medical insurance records to understand how various factors (smoking status, region, sex, BMI, age, number of children) impact insurance charges.

## 🎯 Project Goals

1. **Explore how medical charges differ by:**
   - Smoker vs non-smoker status
   - Geographic region
   - Sex
   - BMI category

2. **Check relationships between:**
   - Age and charges
   - BMI and charges
   - Number of children and charges

3. **Make simple, human-readable conclusions** (not full ML)

## 📁 Project Structure

```
insurance_analysis/
├── insurance.csv                    # Dataset (1,338 records)
├── insurance_analysis.py            # Functional approach (main script)
├── insurance_analysis_class.py      # Object-oriented approach
└── README.md                        # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.6 or higher
- No external dependencies required (uses only standard library)

### Running the Analysis

**Option 1: Functional Approach**
```bash
python insurance_analysis.py
```

**Option 2: Object-Oriented Approach**
```bash
python insurance_analysis_class.py
```

Both scripts produce the same analysis results. The class-based version demonstrates OOP principles and is great for portfolio projects.

## 📊 Dataset Information

The dataset contains the following columns:

- **age**: Age of primary beneficiary
- **sex**: Insurance contractor gender (male/female)
- **bmi**: Body Mass Index
- **children**: Number of children covered by health insurance
- **smoker**: Smoking status (yes/no)
- **region**: Beneficiary's residential area (northeast, northwest, southeast, southwest)
- **charges**: Individual medical costs billed by health insurance

## 🔍 Analysis Features

The scripts perform the following analyses:

1. **Basic Overview**: Summary statistics (count, averages)
2. **Smoker Analysis**: Compare charges between smokers and non-smokers
3. **Regional Analysis**: Compare charges across different US regions
4. **Sex Analysis**: Compare charges between males and females
5. **BMI Category Analysis**: Compare charges across BMI categories (Underweight, Normal, Overweight, Obese)
6. **Age Group Analysis**: Compare charges across age groups
7. **Children Analysis**: Compare charges by number of children
8. **Summary**: Key findings and insights

## 📈 Key Findings

Based on the analysis, you'll discover insights such as:

- **Smoking Impact**: Smokers pay significantly more (typically 200-300% more) than non-smokers
- **Regional Differences**: Some regions have higher average costs than others
- **BMI Impact**: Obese individuals tend to have higher insurance costs
- **Age Correlation**: Older individuals generally have higher insurance costs

## 💻 Code Features

### Functional Version (`insurance_analysis.py`)
- Simple, straightforward functions
- Easy to understand and modify
- Great for learning and quick analysis

### Class-Based Version (`insurance_analysis_class.py`)
- Object-oriented design
- Encapsulated data and methods
- Reusable `InsuranceDataset` class
- Demonstrates OOP principles for portfolios

## 📝 Codecademy Project Checklist

- [x] Create project folder and open in Cursor/IDE
- [x] Put insurance.csv in the folder
- [x] Import csv and read data into lists
- [x] Write mean() helper function
- [x] Print basic overview (num rows, avg age, bmi, charges)
- [x] Analyze charges by smoker vs non-smoker
- [x] Analyze charges by region
- [x] Analyze charges by sex
- [x] Analyze charges by BMI category
- [x] (Optional) Wrap in a class
- [x] (Optional) Publish on GitHub

## 🎓 Learning Outcomes

This project demonstrates:

- CSV file reading and data parsing
- Data manipulation with Python lists
- Statistical analysis (mean calculations)
- Data grouping and aggregation
- Function design and organization
- Object-oriented programming (class version)
- Code documentation and comments

## 📄 License

This project is for educational purposes. The dataset is from Kaggle and is available for analysis.

## 🔗 Resources

- Dataset source: [Kaggle - Medical Cost Personal Datasets](https://www.kaggle.com/datasets/mirichoi0218/insurance)
- Project inspiration: Codecademy Data Science Path

## 👤 Author

Created as part of a portfolio project demonstrating data analysis skills.

---

**Note**: This project is designed to be run locally. For Codecademy submission, mark tasks as complete on the project page. For portfolio purposes, consider hosting on GitHub.

