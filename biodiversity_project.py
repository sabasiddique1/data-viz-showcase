"""
Biodiversity in National Parks – Project Script

You can use this as:

- A standalone .py file, OR
- Copy/paste into Jupyter Notebook cells.

Assumes the following files exist in the same directory:
- species_info.csv
- observations.csv
"""

# =========================
# 1. Imports & Settings
# =========================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

# Plot style
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# =========================
# 2. Load the Data
# =========================

import os
species_path = os.path.join('csv', 'species_info.csv')
observations_path = os.path.join('csv', 'observations.csv')
species = pd.read_csv(species_path)
observations = pd.read_csv(observations_path)

print("=== species_info.csv preview ===")
print(species.head(), "\n")

print("=== observations.csv preview ===")
print(observations.head(), "\n")

print("Species shape:", species.shape)
print("Observations shape:", observations.shape, "\n")

# =========================
# 3. Basic Exploration
# =========================

print("=== Species info ===")
print(species.info(), "\n")

print("Unique categories:", species["category"].unique())
print("Unique conservation statuses:", species["conservation_status"].unique(), "\n")

# How many unique species?
print("Number of unique species:", species["scientific_name"].nunique())

# Fill missing conservation_status with "No Intervention"
species["conservation_status"] = species["conservation_status"].fillna("No Intervention")

print("\n=== conservation_status value counts ===")
print(species["conservation_status"].value_counts())

# =========================
# 4. Distribution of Conservation Status
# =========================

status_counts = (
    species.groupby("conservation_status")["scientific_name"]
    .nunique()
    .reset_index()
    .rename(columns={"scientific_name": "species_count"})
    .sort_values("species_count", ascending=False)
)

print("\n=== Species count by conservation_status ===")
print(status_counts)

plt.figure()
sns.barplot(
    data=status_counts,
    x="conservation_status",
    y="species_count"
)
plt.title("Number of Species by Conservation Status")
plt.xlabel("Conservation Status")
plt.ylabel("Number of Species")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# =========================
# 5. Are Some Categories More Likely to be Protected?
# =========================

# Define "protected" as having any status other than "No Intervention"
species["is_protected"] = species["conservation_status"] != "No Intervention"

category_protection = (
    species.groupby(["category", "is_protected"])["scientific_name"]
    .nunique()
    .reset_index()
    .rename(columns={"scientific_name": "species_count"})
)

print("\n=== Category protection summary ===")
print(category_protection)

# Pivot for easier viewing
category_pivot = category_protection.pivot(
    index="category",
    columns="is_protected",
    values="species_count"
).fillna(0)

category_pivot.columns = ["not_protected", "protected"]
category_pivot["total"] = category_pivot["not_protected"] + category_pivot["protected"]
category_pivot["percent_protected"] = category_pivot["protected"] / category_pivot["total"]

print("\n=== Category pivot (with percent protected) ===")
print(category_pivot)

plt.figure()
sns.barplot(
    data=category_pivot.reset_index(),
    x="category",
    y="percent_protected"
)
plt.title("Percent of Protected Species by Category")
plt.xlabel("Category")
plt.ylabel("Percent Protected")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# =========================
# 6. Chi-Square Tests Between Categories
# =========================

# Example: Mammal vs Bird
def chi_square_between_categories(cat1, cat2):
    """
    Run a chi-square test for protection vs not_protected
    between two categories.
    """

    sub = category_pivot.loc[[cat1, cat2], ["protected", "not_protected"]]
    contingency = sub.values
    chi2, pval, dof, expected = chi2_contingency(contingency)

    print(f"\n=== Chi-Square: {cat1} vs {cat2} ===")
    print("Contingency table:\n", contingency)
    print("Chi2:", chi2)
    print("p-value:", pval)
    print("Degrees of freedom:", dof)
    print("Expected:\n", expected)

    if pval < 0.05:
        print("Result: Significant difference in protection rate.")
    else:
        print("Result: No significant difference in protection rate.")


chi_square_between_categories("Mammal", "Bird")
chi_square_between_categories("Mammal", "Reptile")
chi_square_between_categories("Bird", "Reptile")

# =========================
# 7. Which Species Are Spotted the Most at Each Park?
# =========================

# Merge species info into observations (by scientific_name)
merged = observations.merge(
    species[["scientific_name", "common_name", "category", "is_protected"]],
    on="scientific_name",
    how="left"
)

print("\n=== Merged observations preview ===")
print(merged.head())

# Total observations per species & park
species_park_obs = (
    merged.groupby(["park_name", "common_name", "category", "is_protected"])["observations"]
    .sum()
    .reset_index()
)

print("\n=== Top 10 species by observations (overall) ===")
print(
    species_park_obs
    .sort_values("observations", ascending=False)
    .head(10)
)

# Top 5 most observed species in each park
top_per_park = (
    species_park_obs
    .sort_values(["park_name", "observations"], ascending=[True, False])
    .groupby("park_name")
    .head(5)
)

print("\n=== Top 5 species per park ===")
print(top_per_park)

# Example: barplot for one park
example_park = species_park_obs["park_name"].unique()[0]
print(f"\nPlotting top species for park: {example_park}")

park_data = (
    species_park_obs[species_park_obs["park_name"] == example_park]
    .sort_values("observations", ascending=False)
    .head(10)
)

plt.figure()
sns.barplot(
    data=park_data,
    x="observations",
    y="common_name"
)
plt.title(f"Top Species Observed in {example_park}")
plt.xlabel("Observations (last 7 days)")
plt.ylabel("Species")
plt.tight_layout()
plt.show()

# =========================
# 8. Sample Size / Foot-and-Mouth Disease Study (Template)
# =========================

"""
In the Codecademy project, there is a section about a hypothetical
foot-and-mouth disease study (often using some subset of species like 'Sheep').
Below is a generic template you can adapt once you decide:
- Which species you care about
- Which parks you are comparing
- What minimum detectable effect and baseline rate you assume
"""

# Example: Filtering for sheep-like species (you may need to adjust the filter)
sheep = species[
    species["common_name"].str.contains("Sheep", case=False, na=False)
].copy()

print("\n=== Sheep-related species ===")
print(sheep)

sheep_observations = merged[merged["scientific_name"].isin(sheep["scientific_name"])]

sheep_by_park = (
    sheep_observations
    .groupby("park_name")["observations"]
    .sum()
    .reset_index()
)

print("\n=== Sheep observations by park ===")
print(sheep_by_park)

# -------- Sample size calculation (simple template) --------
# Suppose we want to detect a 5% relative change between two parks.
# You could plug into a standard sample size formula or use statsmodels.
# Here we just leave placeholders.
baseline_rate = 1.0    # placeholder
min_detectable_effect = 0.05  # 5% change
significance_level = 0.05
power = 0.8

print("\n[TODO] Use a sample size calculator or statsmodels to compute:")
print("- Sample size per group for given baseline_rate, MDE, alpha, power")
print("- Then interpret what that means for number of observation days needed.")

# =========================
# 9. High-level textual conclusions (to help with your slide deck)
# =========================

"""
Use these prompts to write your own conclusions (in Markdown / slides):
- What did you learn about the distribution of conservation_status?
- Which categories have the highest percent of protected species?
- Were differences between categories statistically significant? (Chi-square results)
- Which species and parks have the most observations?
- Based on the analysis, what recommendations would you give conservationists?
"""

print("\n=== SCRIPT COMPLETE ===")
print("Now use these outputs & figures to write your conclusions and build your slide deck.")


class Patient:
    def __init__(self, name, age, sex, bmi, num_of_children, smoker):
        self.name = name
        self.age = age
        self.sex = sex              # 0 for male, 1 for female
        self.bmi = bmi
        self.num_of_children = num_of_children
        self.smoker = smoker        # 0 for non-smoker, 1 for smoker

    def estimated_insurance_cost(self):
        estimated_cost = (
            250 * self.age
            - 128 * self.sex
            + 370 * self.bmi
            + 425 * self.num_of_children
            + 24000 * self.smoker
            - 12500
        )
        print(f\"{self.name}'s estimated insurance costs is {estimated_cost} dollars.\")
        return estimated_cost

    def update_age(self, new_age):
        self.age = new_age
        print(f\"{self.name} is now {self.age} years old.\")
        self.estimated_insurance_cost()

    def update_num_children(self, new_num_children):
        self.num_of_children = new_num_children
        if self.num_of_children == 1:
            print(f\"{self.name} has {self.num_of_children} child.\")
        else:
            print(f\"{self.name} has {self.num_of_children} children.\")
        self.estimated_insurance_cost()

    def patient_profile(self):
        patient_information = {
            "name": self.name,
            "age": self.age,
            "sex": self.sex,
            "bmi": self.bmi,
            "num_of_children": self.num_of_children,
            "smoker": self.smoker
        }
        return patient_information


# ----- Test code for the project tasks -----

# Task 2: create first patient instance
patient1 = Patient("John Doe", 25, 1, 22.2, 0, 0)

# Print out patient1's information to verify __init__
print(patient1.name)
print(patient1.age)
print(patient1.sex)
print(patient1.bmi)
print(patient1.num_of_children)
print(patient1.smoker)

# Task 4: test estimated_insurance_cost
patient1.estimated_insurance_cost()

# Task 6–7: test update_age
patient1.update_age(26)

# Task 8–11: test update_num_children
patient1.update_num_children(1)

# Task 12–13: test patient_profile
print(patient1.patient_profile())


# Image Transformations with NumPy
import numpy as np
import matplotlib.pyplot as plt
import codecademylib3

heart_img = np.array([[255, 0, 0, 255, 0, 0, 255],
                      [0, 255/2, 255/2, 0, 255/2, 255/2, 0],
                      [0, 255/2, 255/2, 255/2, 255/2, 255/2, 0],
                      [0, 255/2, 255/2, 255/2, 255/2, 255/2, 0],
                      [255, 0, 255/2, 255/2, 255/2, 0, 255],
                      [255, 255, 0, 255/2, 0, 255, 255],
                      [255, 255, 255, 0, 255, 255, 255]])


# This is a helper function that makes it easy for you to show images!
def show_image(image, name_identifier):
    plt.imshow(image, cmap="gray")
    plt.title(name_identifier)
    plt.show()


# Show heart image
show_image(heart_img, "Heart Image")

# Invert color
inverted_heart_img = 255 - heart_img
show_image(inverted_heart_img, "Inverted Heart Image")

# Rotate heart (transpose: swap rows and columns)
rotated_heart_img = heart_img.T
show_image(rotated_heart_img, "Rotated Heart Image")

# Random Image
random_img = np.random.randint(0, 255, (7, 7))
show_image(random_img, "Random Image")

# Solve for heart image
# random_img · x = heart_img  =>  x = random_img^{-1} · heart_img
x = np.linalg.solve(random_img, heart_img)
show_image(x, "x")

solved_heart_img = random_img.dot(x)
show_image(solved_heart_img, "Solved Heart Image")

heart_img = np.array([[255, 0, 0, 255, 0, 0, 255],          # row 0
                      [0, 255/2, 255/2, 0, 255/2, 255/2, 0],        # row 1
                      [0, 255/2, 255/2, 255/2, 255/2, 255/2, 0],        # row 2
                      [0, 255/2, 255/2, 255/2, 255/2, 255/2, 0],        # row 3
                      [255, 0, 255/2, 255/2, 255/2, 0, 255],        # row 4
                      [255, 255, 0, 255/2, 0, 255, 255],        # row 5
                      [255, 255, 255, 0, 255, 255, 255]])       # row 6


# Limit Definition of the Derivative Exploration

import numpy as np
import codecademylib3
from math import sin, cos, log, pi
import matplotlib.pyplot as plt


# --------------------------------------------------
# Limit definition of the derivative
# --------------------------------------------------

def limit_derivative(f, x, h):
    """
    f: function to be differentiated
    x: the point at which to differentiate f
    h: distance between the points to be evaluated
    """
    return (f(x + h) - f(x)) / h


# --------------------------------------------------
# Define functions
# --------------------------------------------------

# f1(x) = sin(x)
def f1(x):
    return sin(x)


# f2(x) = x^4
def f2(x):
    return pow(x, 4)


# f3(x) = x^2 * ln(x)
def f3(x):
    return pow(x, 2) * log(x)


# --------------------------------------------------
# Task 2 & 3: Approximate derivative of f3 at x = 1
# --------------------------------------------------

print(limit_derivative(f3, 1, 2))
print(limit_derivative(f3, 1, 0.1))
print(limit_derivative(f3, 1, 0.00001))


# --------------------------------------------------
# Graphing helper function
# --------------------------------------------------

def plot_approx_deriv(f):
    x_vals = np.linspace(1, 10, 200)
    h_vals = [10, 1, 0.25, 0.01]
    for h in h_vals:
        derivative_values = []
        for x in x_vals:
            derivative_values.append(limit_derivative(f, x, h))
        plt.plot(
            x_vals,
            derivative_values,
            linestyle='--',
            label="h=" + str(h)
        )
    plt.legend()
    plt.title("Convergence to Derivative by varying h")
    plt.show()


# --------------------------------------------------
# GRAPH 1: f1(x) = sin(x), true derivative = cos(x)
# --------------------------------------------------

x_vals = np.linspace(1, 10, 200)
y_vals = [cos(val) for val in x_vals]
plt.figure(1)
plt.plot(x_vals, y_vals, label="True Derivative", linewidth=4)
plot_approx_deriv(f1)


# --------------------------------------------------
# GRAPH 2: f2(x) = x^4, true derivative = 4x^3
# --------------------------------------------------

y_vals = [4 * (val ** 3) for val in x_vals]
plt.figure(2)
plt.plot(x_vals, y_vals, label="True Derivative", linewidth=4)
plot_approx_deriv(f2)


# Heart Disease Research Part II

# ---------------------------------------
# Heart Disease Research Part II
# ---------------------------------------

import codecademylib3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, f_oneway, chi2_contingency
from statsmodels.stats.multicomp import pairwise_tukeyhsd


# ---------------------------------------
# Load data
# ---------------------------------------

import os
heart_path = os.path.join('csv', 'heart_disease.csv')
heart = pd.read_csv(heart_path)


# ---------------------------------------
# Task 1: Inspect data
# ---------------------------------------

print(heart.head())


# ---------------------------------------
# Task 2: thalach vs heart disease (boxplot)
# ---------------------------------------

sns.boxplot(x=heart.heart_disease, y=heart.thalach)
plt.show()


# ---------------------------------------
# Task 3: Separate thalach groups
# ---------------------------------------

thalach_hd = heart.thalach[heart.heart_disease == 'presence']
thalach_no_hd = heart.thalach[heart.heart_disease == 'absence']


# ---------------------------------------
# Task 4: Mean & median differences
# ---------------------------------------

print("Mean difference:", np.mean(thalach_hd) - np.mean(thalach_no_hd))
print("Median difference:", np.median(thalach_hd) - np.median(thalach_no_hd))


# ---------------------------------------
# Task 5 & 6: Two-sample t-test (thalach)
# ---------------------------------------

tstat, pval = ttest_ind(thalach_hd, thalach_no_hd)
print("Thalach p-value:", pval)


# ---------------------------------------
# Task 7: Investigate age
# ---------------------------------------

plt.clf()
sns.boxplot(x=heart.heart_disease, y=heart.age)
plt.show()

age_hd = heart.age[heart.heart_disease == 'presence']
age_no_hd = heart.age[heart.heart_disease == 'absence']
print("Age p-value:", ttest_ind(age_hd, age_no_hd)[1])


# ---------------------------------------
# Task 8: thalach vs chest pain type
# ---------------------------------------

plt.clf()
sns.boxplot(x=heart.cp, y=heart.thalach)
plt.show()


# ---------------------------------------
# Task 9: Separate chest pain groups
# ---------------------------------------

thalach_typical = heart.thalach[heart.cp == 'typical angina']
thalach_asymptom = heart.thalach[heart.cp == 'asymptomatic']
thalach_nonangin = heart.thalach[heart.cp == 'non-anginal pain']
thalach_atypical = heart.thalach[heart.cp == 'atypical angina']


# ---------------------------------------
# Task 10: ANOVA on chest pain types
# ---------------------------------------

fstat, pval = f_oneway(
    thalach_typical,
    thalach_asymptom,
    thalach_nonangin,
    thalach_atypical
)
print("ANOVA p-value:", pval)


# ---------------------------------------
# Task 11: Tukey's Range Test
# ---------------------------------------

thalach_vals = heart.thalach
cp_vals = heart.cp
tukey = pairwise_tukeyhsd(thalach_vals, cp_vals, alpha=0.05)
print(tukey)


# ---------------------------------------
# Task 12: Contingency table (cp vs heart disease)
# ---------------------------------------

Xtab = pd.crosstab(heart.cp, heart.heart_disease)
print(Xtab)


# ---------------------------------------
# Task 13: Chi-Square test
# ---------------------------------------

chi2, pval, dof, expected = chi2_contingency(Xtab)
print("Chi-square p-value:", pval)


# ---------------------------------------
# Task 14: Further exploration (example: sex)
# ---------------------------------------

Xtab_sex = pd.crosstab(heart.sex, heart.heart_disease)
print(Xtab_sex)
print("Sex vs heart disease p-value:",
      chi2_contingency(Xtab_sex)[1])


# A/B Testing at Nosh Mish Mosh

# ---------------------------------------
# A/B Testing at Nosh Mish Mosh
# ---------------------------------------

# Task 1: import noshmishmosh
import codecademylib3
import noshmishmosh

# Task 2: import numpy
import numpy as np


# ---------------------------------------
# Baseline Conversion Rate
# ---------------------------------------

# Task 4: all visitors
all_visitors = noshmishmosh.customer_visits

# Task 5: paying visitors
paying_visitors = noshmishmosh.purchasing_customers

# Task 6: count visitors
total_visitor_count = len(all_visitors)
paying_visitor_count = len(paying_visitors)

# Task 7: baseline percentage
baseline_percent = (paying_visitor_count / total_visitor_count) * 100.0

# Task 8: print baseline
print("Baseline Conversion Rate (%):", baseline_percent)


# ---------------------------------------
# Effect Size (Minimum Detectable Effect)
# ---------------------------------------

# Task 9: payment history
payment_history = noshmishmosh.money_spent

# Task 10: average payment
average_payment = np.mean(payment_history)

# Task 11: customers needed for $1240
new_customers_needed = np.ceil(1240 / average_payment)

# Task 12: percentage point increase
percentage_point_increase = (new_customers_needed / total_visitor_count) * 100
print("Percentage Point Increase (%):", percentage_point_increase)

# Task 13: minimum detectable effect
mde = (percentage_point_increase / baseline_percent) * 100.0

# Task 14: print MDE
print("Minimum Detectable Effect (%):", mde)


# ---------------------------------------
# Statistical Significance & Sample Size
# ---------------------------------------

# Task 15: significance threshold
significance_threshold = 10

# Task 16: sample size calculation
ab_sample_size = noshmishmosh.calculate_sample_size(
    baseline_percent,
    mde,
    significance_threshold
)
print("Required A/B Sample Size:", ab_sample_size)


# Familiar: A Study In Data Analysis

# In familiar


